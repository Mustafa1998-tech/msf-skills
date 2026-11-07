IF DB_ID(N'MsfInventoryDemo') IS NULL
    CREATE DATABASE MsfInventoryDemo;
GO
USE MsfInventoryDemo;
GO
SET XACT_ABORT ON;
BEGIN TRANSACTION;
IF OBJECT_ID(N'dbo.InventoryItem', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.InventoryCategory (
        Code varchar(16) NOT NULL CONSTRAINT PK_InventoryCategory PRIMARY KEY,
        NameAr nvarchar(80) NOT NULL,
        NameEn nvarchar(80) NOT NULL
    );
    CREATE TABLE dbo.InventoryItem (
        Id int IDENTITY(1,1) NOT NULL CONSTRAINT PK_InventoryItem PRIMARY KEY,
        Sku varchar(24) NOT NULL CONSTRAINT UQ_InventoryItem_Sku UNIQUE,
        NameAr nvarchar(80) NOT NULL,
        NameEn nvarchar(80) NOT NULL,
        CategoryCode varchar(16) NOT NULL
            CONSTRAINT FK_InventoryItem_Category REFERENCES dbo.InventoryCategory(Code),
        Quantity int NOT NULL CONSTRAINT CK_InventoryItem_Quantity CHECK (Quantity BETWEEN 0 AND 1000000),
        Archived bit NOT NULL CONSTRAINT DF_InventoryItem_Archived DEFAULT (0),
        UpdatedAt datetime2(0) NOT NULL CONSTRAINT DF_InventoryItem_UpdatedAt DEFAULT (SYSUTCDATETIME()),
        UpdatedBy varchar(32) NOT NULL,
        Version rowversion NOT NULL
    );
    CREATE INDEX IX_InventoryItem_Archived_Id ON dbo.InventoryItem (Archived, Id DESC);
    INSERT dbo.InventoryCategory (Code,NameAr,NameEn) VALUES
        ('TOOLS', N'الأدوات', N'Tools'), ('SAFETY', N'السلامة', N'Safety'),
        ('PARTS', N'قطع الغيار', N'Spare parts');
    INSERT dbo.InventoryItem (Sku,NameAr,NameEn,CategoryCode,Quantity,UpdatedBy) VALUES
        ('WT-031', N'مفتاح عزم', N'Torque wrench','TOOLS',14,'seed'),
        ('SG-104', N'نظارات واقية', N'Safety goggles','SAFETY',32,'seed'),
        ('FS-220', N'مجموعة مثبتات', N'Fastener set','PARTS',4,'seed');
END;
COMMIT TRANSACTION;
GO
-- Optional after mapping a dedicated login to a database user:
-- CREATE ROLE inventory_api;
-- GRANT SELECT ON dbo.InventoryCategory TO inventory_api;
-- GRANT SELECT, INSERT, UPDATE ON dbo.InventoryItem TO inventory_api;
-- ALTER ROLE inventory_api ADD MEMBER [your_inventory_app_user];
