use Dealership
go

create or alter procedure UploadVehicles(

	@file as varchar(200)
)
as
begin

	drop table [Dealership].[dbo].[Vehicles];

	CREATE TABLE [Dealership].[dbo].[Vehicles](
	[Vehicle_Id] [int] IDENTITY(1,1) NOT NULL,
	[Model] [varchar](20) NOT NULL,
	[Year] [int] NOT NULL,
	[Colour] [varchar](20) NOT NULL,
	[Engine_Capacity] [decimal](4,2) NOT NULL,
	[Wheel_Size] [tinyint] NOT NULL,
	[Mileage] [int] NOT NULL,
	[Fuel_Type] [varchar](20) NOT NULL,
	[Top_Speed] [smallint] NOT NULL,
	[Previous_Owners] [int] NOT NULL,
	[Service_History] [varchar](20) NOT NULL,
	[Horsepower] [smallint] NOT NULL,
	[Vehicle_Vin] [char](17) NOT NULL,
	[Automatic_Transmission] [bit] NOT NULL,
	[Manufacturer_Id] [int] NOT NULL,
	[Image_Id] [int]
	);
	
	Declare @JSON varchar(max);
	Declare @SQL nvarchar(max);

	set @SQL = 'SELECT @JSON=BulkColumn FROM OPENROWSET (BULK ''' + @file + ''',  SINGLE_CLOB) as import';

	exec sys.sp_executesql @SQL, N'@JSON varchar(max) OUTPUT', @JSON OUTPUT;

	INSERT INTO [Dealership].[dbo].[Vehicles]
	SELECT *
	FROM OPENJSON (@JSON)
	WITH 
	(
	[Model] [varchar](20), 
	[Year] [int], 
	[Colour] [varchar](20), 
	[Engine_Capacity] [decimal](4,2), 
	[Wheel_Size] [tinyint], 
	[Mileage] [int], 
	[Fuel_Type] [varchar](20), 
	[Top_Speed] [smallint], 
	[Previous_Owners] [int], 
	[Service_History] [varchar](20), 
	[Horsepower] [smallint],
	[Vehicle_Vin] [char](17), 
	[Automatic_Transmission] [bit],
	[Manufacturer_Id] [varchar](20), 
	[Image_Id] [varchar](60)
	);

end;
go

create or alter procedure UploadManufacturers(

	@file as varchar(200)
)
as
begin
	
	drop table [Dealership].[dbo].[Manufacturers];

	CREATE TABLE  [Dealership].[dbo].[Manufacturers](
	[Manufacturer_Id] [int] IDENTITY(1,1) NOT NULL,
	[Name] [varchar](50) NOT NULL,
	[Phone_Number] [varchar](16) NOT NULL,
	[Email] [varchar](50) NOT NULL
	);
	
	Declare @JSON varchar(max);
	Declare @SQL nvarchar(max);

	set @SQL = 'SELECT @JSON=BulkColumn FROM OPENROWSET (BULK ''' + @file + ''',  SINGLE_CLOB) as import';

	exec sys.sp_executesql @SQL, N'@JSON varchar(max) OUTPUT', @JSON OUTPUT;

	INSERT INTO [Dealership].[dbo].[Manufacturers]
	SELECT *
	FROM OPENJSON (@JSON)
	WITH 
	(
	[Name] [varchar](50),
	[Phone_Number] [varchar](16),
	[Email] [varchar](50)
	);

end;
go

create or alter procedure UploadVehicle_Images(

	@file as varchar(200)
)
as
begin
	
	drop table [Dealership].[dbo].[Vehicle_Images];

	CREATE TABLE  [Dealership].[dbo].[Vehicle_Images](
	[Image_Id] [int] IDENTITY(1,1) NOT NULL,
	[Vehicle_Id] [int] NOT NULL,
	[Image] [varbinary](max) NOT NULL
	);
	
	Declare @JSON varchar(max);
	Declare @SQL nvarchar(max);

	set @SQL = 'SELECT @JSON=BulkColumn FROM OPENROWSET (BULK ''' + @file + ''',  SINGLE_CLOB) as import';

	exec sys.sp_executesql @SQL, N'@JSON varchar(max) OUTPUT', @JSON OUTPUT;

	INSERT INTO [Dealership].[dbo].[Vehicle_Images]
	SELECT *
	FROM OPENJSON (@JSON)
	WITH 
	(
	[Vehicle_Id] [int],
	[Image] [varbinary](max)
	);

end;
go

create or alter procedure UploadVehicle_Extras(

	@file as varchar(200)
)
as
begin
	
	drop table [Dealership].[dbo].[Vehicle_Extras];

	CREATE TABLE  [Dealership].[dbo].[Vehicle_Extras](
	[Extra_Id] [int] NOT NULL,
	[Vehicle_Id] [int] NOT NULL
	);
	
	Declare @JSON varchar(max);
	Declare @SQL nvarchar(max);

	set @SQL = 'SELECT @JSON=BulkColumn FROM OPENROWSET (BULK ''' + @file + ''',  SINGLE_CLOB) as import';

	exec sys.sp_executesql @SQL, N'@JSON varchar(max) OUTPUT', @JSON OUTPUT;

	INSERT INTO [Dealership].[dbo].[Vehicle_Extras]
	SELECT *
	FROM OPENJSON (@JSON)
	WITH 
	(
	[Extra_Id] [int],
	[Vehicle_Id] [int]
	);

end;
go