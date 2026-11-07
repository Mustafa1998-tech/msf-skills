# Field procedure

Keep DTOs explicit and derive the principal and tenant from trusted authentication. Scope queries before returning data. Consider optimistic concurrency via row version/ETag when conflicting edits matter and define 409 or 412 consistently. Record a bounded timeout per outbound integration and choose a retry only when safe. Test a hub connection, reconnect and rejected unauthorized send in a disposable environment.
