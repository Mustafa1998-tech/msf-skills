using System.Data;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using Microsoft.AspNetCore.Diagnostics;
using Microsoft.Data.SqlClient;

var builder = WebApplication.CreateBuilder(args);
if (!builder.Environment.IsDevelopment())
    throw new InvalidOperationException("This sample uses local demo credentials and only runs in Development.");
var connection = builder.Configuration.GetConnectionString("Inventory")
    ?? throw new InvalidOperationException("Set ConnectionStrings__Inventory.");
var readerKey = builder.Configuration["Inventory:ReaderKey"];
var editorKey = builder.Configuration["Inventory:EditorKey"];
if (string.IsNullOrWhiteSpace(readerKey) || string.IsNullOrWhiteSpace(editorKey)
    || readerKey.Length < 24 || editorKey.Length < 24 || readerKey == editorKey)
    throw new InvalidOperationException("Set two distinct demo keys of at least 24 characters.");
byte[] readerDigest = Hash(readerKey), editorDigest = Hash(editorKey);
builder.Services.AddProblemDetails();
var app = builder.Build();
app.UseExceptionHandler(error => error.Run(async context =>
{
    var failure = context.Features.Get<IExceptionHandlerFeature>()?.Error;
    await (failure is BadHttpRequestException badRequest
        ? Problem(badRequest.StatusCode, "invalid_request", "The request could not be read.")
        : Problem(500, "unexpected_error", "The request failed.")).ExecuteAsync(context);
}));
app.UseStatusCodePages(async status =>
{
    var context = status.HttpContext;
    await Problem(context.Response.StatusCode, "invalid_request", "The request could not be completed.").ExecuteAsync(context);
});
app.Use(async (HttpContext context, Func<Task> next) =>
{
    if (!context.Request.Path.StartsWithSegments("/api")) { await next(); return; }
    context.Response.Headers.CacheControl = "no-store";
    var authorization = context.Request.Headers.Authorization.ToString();
    var presented = authorization.StartsWith("Bearer ", StringComparison.OrdinalIgnoreCase)
        ? Hash(authorization[7..]) : Array.Empty<byte>();
    var canEdit = CryptographicOperations.FixedTimeEquals(presented, editorDigest);
    var canRead = CryptographicOperations.FixedTimeEquals(presented, readerDigest);
    if (!canEdit && !canRead)
    {
        context.Response.Headers.WWWAuthenticate = "Bearer";
        await Problem(401, "sign_in_required", "Enter a valid local demo key.").ExecuteAsync(context);
        return;
    }
    if (!canEdit && !HttpMethods.IsGet(context.Request.Method))
    {
        await Problem(403, "write_forbidden", "An editor key is required for this change.").ExecuteAsync(context);
        return;
    }
    await next();
});

app.MapGet("/health/ready", async (CancellationToken ct) =>
{
    try
    {
        await using var db = await Open(ct);
        await using var command = db.CreateCommand();
        command.CommandText = "SELECT TOP (1) Code FROM dbo.InventoryCategory;";
        await command.ExecuteScalarAsync(ct);
        return Results.Ok(new { status = "ready" });
    }
    catch (SqlException) { return Problem(503, "database_unavailable", "Inventory database is unavailable."); }
});
app.MapGet("/api/categories", async (CancellationToken ct) =>
{
    await using var db = await Open(ct);
    await using var command = db.CreateCommand();
    command.CommandText = "SELECT Code,NameAr,NameEn FROM dbo.InventoryCategory ORDER BY Code;";
    await using var sql = await command.ExecuteReaderAsync(ct);
    var results = new List<Category>();
    while (await sql.ReadAsync(ct)) results.Add(new(sql.GetString(0), sql.GetString(1), sql.GetString(2)));
    return Results.Ok(results);
});
app.MapGet("/api/items", async (string? q, string? category, bool? archived, int? before, CancellationToken ct) =>
{
    q = (q ?? "").Trim();
    category = (category ?? "").Trim();
    if (q.Length > 80 || category.Length > 16 || before <= 0)
        return Problem(400, "invalid_filter", "Check search, category and page cursor.");
    await using var db = await Open(ct);
    await using var command = db.CreateCommand();
    command.CommandText = """
        SELECT TOP (25) Id,Sku,NameAr,NameEn,CategoryCode,Quantity,Archived,Version
        FROM dbo.InventoryItem
        WHERE Archived=@archived AND (@before IS NULL OR Id < @before)
          AND (@category='' OR CategoryCode=@category)
          AND (@q=N'' OR CHARINDEX(@q,Sku)>0 OR CHARINDEX(@q,NameAr)>0 OR CHARINDEX(@q,NameEn)>0)
        ORDER BY Id DESC;
        """;
    Add(command, "@archived", SqlDbType.Bit, archived ?? false);
    Add(command, "@before", SqlDbType.Int, before is null ? DBNull.Value : (object)before.Value);
    Add(command, "@q", SqlDbType.NVarChar, q, 80);
    Add(command, "@category", SqlDbType.VarChar, category, 16);
    await using var sql = await command.ExecuteReaderAsync(ct);
    var results = new List<Item>();
    while (await sql.ReadAsync(ct)) results.Add(Read(sql));
    return Results.Ok(results);
});
app.MapGet("/api/items/{id:int}", async (int id, CancellationToken ct) =>
{
    await using var db = await Open(ct);
    await using var command = db.CreateCommand();
    command.CommandText = "SELECT Id,Sku,NameAr,NameEn,CategoryCode,Quantity,Archived,Version FROM dbo.InventoryItem WHERE Id=@id;";
    Add(command, "@id", SqlDbType.Int, id);
    await using var sql = await command.ExecuteReaderAsync(ct);
    return await sql.ReadAsync(ct) ? Results.Ok(Read(sql)) : Problem(404, "item_missing", "Item does not exist.");
});
app.MapPost("/api/items", (ItemInput input, CancellationToken ct) => Save(null, input, ct));
app.MapPut("/api/items/{id:int}", (int id, ItemInput input, CancellationToken ct) => Save(id, input, ct));
app.MapPost("/api/items/{id:int}/archive", (int id, VersionInput input, CancellationToken ct) => Transition(id, input, true, ct));
app.MapPost("/api/items/{id:int}/restore", (int id, VersionInput input, CancellationToken ct) => Transition(id, input, false, ct));
app.Run();

async Task<SqlConnection> Open(CancellationToken ct)
{
    var db = new SqlConnection(connection);
    try { await db.OpenAsync(ct); return db; }
    catch { await db.DisposeAsync(); throw; }
}
async Task<IResult> Save(int? id, ItemInput input, CancellationToken ct)
{
    var sku = (input.Sku ?? "").Trim().ToUpperInvariant();
    var ar = (input.NameAr ?? "").Trim();
    var en = (input.NameEn ?? "").Trim();
    var category = (input.CategoryCode ?? "").Trim();
    if (!Regex.IsMatch(sku, "^[A-Z0-9-]{1,24}$", RegexOptions.CultureInvariant)
        || ar.Length is < 1 or > 80 || en.Length is < 1 or > 80
        || category.Length is < 1 or > 16 || input.Quantity is null or < 0 or > 1000000)
        return Problem(400, "invalid_item", "Provide SKU, names, category and quantity from 0 to 1000000.");
    var version = ParseVersion(input.Version);
    if (id.HasValue && version is null)
        return Problem(400, "invalid_version", "Reload the item to get its current version.");
    try
    {
        await using var db = await Open(ct);
        await using var command = db.CreateCommand();
        command.CommandText = id.HasValue ? """
            UPDATE dbo.InventoryItem SET Sku=@sku,NameAr=@ar,NameEn=@en,CategoryCode=@category,
                Quantity=@quantity,UpdatedAt=SYSUTCDATETIME(),UpdatedBy='demo-editor'
            OUTPUT inserted.Id,inserted.Sku,inserted.NameAr,inserted.NameEn,inserted.CategoryCode,
                inserted.Quantity,inserted.Archived,inserted.Version
            WHERE Id=@id AND Version=@version AND Archived=0;
            """ : """
            INSERT dbo.InventoryItem (Sku,NameAr,NameEn,CategoryCode,Quantity,UpdatedBy)
            OUTPUT inserted.Id,inserted.Sku,inserted.NameAr,inserted.NameEn,inserted.CategoryCode,
                inserted.Quantity,inserted.Archived,inserted.Version
            VALUES (@sku,@ar,@en,@category,@quantity,'demo-editor');
            """;
        Add(command, "@sku", SqlDbType.VarChar, sku, 24);
        Add(command, "@ar", SqlDbType.NVarChar, ar, 80);
        Add(command, "@en", SqlDbType.NVarChar, en, 80);
        Add(command, "@category", SqlDbType.VarChar, category, 16);
        Add(command, "@quantity", SqlDbType.Int, input.Quantity.Value);
        if (id.HasValue)
        {
            Add(command, "@id", SqlDbType.Int, id.Value);
            Add(command, "@version", SqlDbType.Binary, version!, 8);
        }
        await using var sql = await command.ExecuteReaderAsync(ct);
        if (!await sql.ReadAsync(ct)) return Conflict();
        var item = Read(sql);
        return id.HasValue ? Results.Ok(item) : Results.Created($"/api/items/{item.Id}", item);
    }
    catch (SqlException e) when (e.Number is 2601 or 2627) { return Problem(409, "sku_exists", "The SKU is already assigned."); }
    catch (SqlException e) when (e.Number == 547) { return Problem(400, "invalid_category", "Choose an existing category."); }
}
async Task<IResult> Transition(int id, VersionInput input, bool archived, CancellationToken ct)
{
    var version = ParseVersion(input.Version);
    if (version is null) return Problem(400, "invalid_version", "Reload the item to get its current version.");
    await using var db = await Open(ct);
    await using var command = db.CreateCommand();
    command.CommandText = """
        UPDATE dbo.InventoryItem SET Archived=@archived,UpdatedAt=SYSUTCDATETIME(),UpdatedBy='demo-editor'
        OUTPUT inserted.Id,inserted.Sku,inserted.NameAr,inserted.NameEn,inserted.CategoryCode,
            inserted.Quantity,inserted.Archived,inserted.Version
        WHERE Id=@id AND Version=@version AND Archived<>@archived;
        """;
    Add(command, "@id", SqlDbType.Int, id);
    Add(command, "@archived", SqlDbType.Bit, archived);
    Add(command, "@version", SqlDbType.Binary, version, 8);
    await using var sql = await command.ExecuteReaderAsync(ct);
    return await sql.ReadAsync(ct) ? Results.Ok(Read(sql)) : Conflict();
}
static Item Read(SqlDataReader sql) => new(sql.GetInt32(0), sql.GetString(1), sql.GetString(2), sql.GetString(3),
    sql.GetString(4), sql.GetInt32(5), sql.GetBoolean(6), Convert.ToBase64String((byte[])sql.GetValue(7)));
static void Add(SqlCommand command, string name, SqlDbType type, object value, int length = 0) =>
    command.Parameters.Add(name, type, length).Value = value;
static byte[] Hash(string text) => SHA256.HashData(Encoding.UTF8.GetBytes(text));
static byte[]? ParseVersion(string? text) =>
    text is { Length: 12 } && Convert.TryFromBase64String(text, new byte[8], out var length) && length == 8
        ? Convert.FromBase64String(text) : null;
static IResult Conflict() => Problem(409, "item_conflict", "The item changed or is not in the required state. Reload the list.");
static IResult Problem(int status, string code, string title) =>
    Results.Problem(title: title, statusCode: status, extensions: new Dictionary<string, object?> { ["code"] = code });

record Category(string Code, string NameAr, string NameEn);
record Item(int Id, string Sku, string NameAr, string NameEn, string CategoryCode, int Quantity, bool Archived, string Version);
record ItemInput(string? Sku, string? NameAr, string? NameEn, string? CategoryCode, int? Quantity, string? Version);
record VersionInput(string? Version);
