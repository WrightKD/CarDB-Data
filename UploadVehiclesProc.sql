use Dealership;
go

create or alter procedure UploadVehicles(

	@file as varchar(200)
)
as
begin

	if OBJECT_ID('[Dealership].[dbo].[Cars]','U') is not null
		drop table [Dealership].[dbo].[Cars];
	
	Declare @JSON varchar(max);
	Declare @SQL nvarchar(max);

	set @SQL = 'SELECT @JSON=BulkColumn FROM OPENROWSET (BULK ''' + @file + ''',  SINGLE_CLOB) as import';

	exec sys.sp_executesql @SQL, N'@JSON varchar(max) OUTPUT', @JSON OUTPUT;

	SELECT * INTO Cars
	FROM OPENJSON (@JSON)
	WITH 
	(
    [Model] varchar(20), 
    [Price] varchar(20), 
    [Type] varchar(20), 
    [Year] int, 
    [Mileage] varchar(20),
    [Gearbox] varchar(20),
    [Dealer] varchar(20),
    [Suburb] varchar(20)
	);

end;
go