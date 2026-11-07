# Raff: inventory ledger

[العربية](README.ar.md) · [Worked skill routing and release evidence](WORKFLOW.md)

Raff is a synthetic inventory feature for a warehouse team. It combines a bilingual Angular UI, an ASP.NET Core minimal API, and a SQL Server schema. The workflow covers item creation, searchable lists and category options, editing, and an archive/restore cycle that retains the SKU and rejects stale updates. Arabic and RTL are the defaults.

| Layer | Entry point | What to look for |
| --- | --- | --- |
| Angular | [web/src/inventory.html](web/src/inventory.html) | RTL, bilingual labels and errors, searchable category picker, empty/loading/error states |
| ASP.NET Core | [api/Program.cs](api/Program.cs) | Stable error codes, server authorization, bounded inputs, version checks |
| SQL Server | [sql/001-inventory.sql](sql/001-inventory.sql) | Unicode names, unique SKU, FK and quantity constraints, archive index, rowversion |
| Integration test | [tests/smoke.mjs](tests/smoke.mjs) | Authorization, validation, literal search, concurrency, archive/restore |

## Run locally

Use a disposable local SQL Server instance, `sqlcmd`, the .NET 10 SDK, Node 22.12+ (22.x) or Node 24.x, and a browser. Run these commands from this example's directory. The process is for a local machine only; the API refuses to start outside Development.

1. Use your own local SQL credentials to create and seed `MsfInventoryDemo`. This command prompts for the SQL password when it is not already supplied through the SQL client environment:

   ```sh
   sqlcmd -S localhost,1433 -U YOUR_SETUP_LOGIN -C -b -i sql/001-inventory.sql
   ```

   The setup login needs database creation privileges. For the API, map a different login to a database user and grant the table permissions listed at the end of the script. The sample does not require or grant `DELETE`. The `-C` switch is for this disposable instance with a local self-signed certificate.

2. Set a connection string for that application user using your shell or a local secret manager. For a local, self-signed developer instance its form is `Server=localhost,1433;Database=MsfInventoryDemo;User Id=…;Password=…;Encrypt=True;TrustServerCertificate=True`. Start the API with two independently generated local keys:

   ```sh
   export ASPNETCORE_ENVIRONMENT=Development
   export Inventory__ReaderKey="$(openssl rand -hex 24)"
   export Inventory__EditorKey="$(openssl rand -hex 24)"
   # Set/export ConnectionStrings__Inventory with your local connection string.
   dotnet run --project api --no-launch-profile --urls http://127.0.0.1:5080
   ```

3. In another terminal, run:

   ```sh
   cd web
   npm ci
   npm start
   ```

   Open `http://127.0.0.1:4200`. Enter the local reader or editor key from step 2. Use the editor key for changes. The browser keeps the key in memory until disconnect or reload; the Angular dev server proxies `/api/**` to the API.

4. To check the backend with the same two environment variables as the API, open another terminal, export the original keys, and run:

   ```sh
   node tests/smoke.mjs
   ```

   The test creates a unique synthetic SKU and leaves it archived. It covers 401 and 403, validation, duplicate SKU, literal SQL-like text search, stale editing, archive visibility, and restore. Run it only against the disposable instance.

## Try the workflow

1. Search by `WT-031` or `مفتاح عزم`. Open the category picker and find the Tools option by typing its code or either name.
2. Add a SKU with both names, edit its quantity, and try entering the same SKU again to see the explicit error.
3. Archive the item, switch to the archive list, and restore it. The item keeps its ID and SKU.
4. Open the same edit in two tabs and save one before the other. The second receives a conflict and asks the operator to reload.

This sample has no external identity provider or tenant isolation. The two demo keys represent shared local roles, and the writer marker identifies the demo role only. Before using this pattern with real inventory, add production identity, individual audit events and review, proper TLS, secret rotation, operational limits, a migration pipeline, and the release gates in [WORKFLOW.md](WORKFLOW.md).

References: [Angular version compatibility](https://angular.dev/reference/versions), [Angular proxy configuration](https://angular.dev/tools/cli/serve), and [SQL Server rowversion](https://learn.microsoft.com/en-us/sql/t-sql/data-types/rowversion-transact-sql).

## Additional verification

Run `node tests/boundary.mjs` with the API and the two local keys to check authentication and request validation before SQL access. This check does not require a running database, but the API still requires a connection string to start.

The optional [browser check](tests/browser.mjs) verifies the Angular experience with simulated API responses. Install Playwright in the example root with `npm install --no-save playwright` and `npx playwright install chromium`. Start the Angular dev server, then run `node tests/browser.mjs` from the example root. This is separate from the SQL-backed test.
