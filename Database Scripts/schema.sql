/****** Object:  Table [dbo].[Addresses]    Script Date: 8/23/2025 1:43:46 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Addresses](
	[AddressId] [int] IDENTITY(1,1) NOT NULL,
	[AddressType] [nvarchar](20) NOT NULL,
	[AddressLine1] [nvarchar](100) NOT NULL,
	[AddressLine2] [nvarchar](255) NULL,
	[City] [nvarchar](50) NOT NULL,
	[StateCode] [nchar](2) NOT NULL,
	[ZipCode] [nvarchar](10) NOT NULL,
	[County] [nvarchar](100) NULL,
	[Country] [nvarchar](100) NULL,
	[IsActive] [bit] NOT NULL,
	[CreatedDate] [datetime2](7) NOT NULL,
 CONSTRAINT [PK__Addresse__091C2AFBA770B436] PRIMARY KEY CLUSTERED 
(
	[AddressId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[CustomerAddresses]    Script Date: 8/23/2025 1:43:46 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[CustomerAddresses](
	[CustomerAddressId] [int] IDENTITY(1,1) NOT NULL,
	[CustomerId] [int] NOT NULL,
	[AddressId] [int] NOT NULL,
	[IsPrimary] [bit] NOT NULL,
	[CreatedDate] [datetime2](7) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[CustomerAddressId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Customers]    Script Date: 8/23/2025 1:43:46 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Customers](
	[CustomerId] [int] IDENTITY(1,1) NOT NULL,
	[CustomerCode] [nvarchar](20) NOT NULL,
	[CompanyName] [nvarchar](255) NOT NULL,
	[ContactFirstName] [nvarchar](100) NULL,
	[ContactLastName] [nvarchar](100) NULL,
	[Email] [nvarchar](255) NULL,
	[Phone] [nvarchar](20) NULL,
	[Fax] [nvarchar](20) NULL,
	[Website] [nvarchar](255) NULL,
	[IsActive] [bit] NOT NULL,
	[CreatedDate] [datetime2](7) NOT NULL,
	[ModifiedDate] [datetime2](7) NOT NULL,
	[CreatedBy] [nvarchar](100) NULL,
	[ModifiedBy] [nvarchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[CustomerId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[CustomerCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[GeocodedIDs]    Script Date: 8/23/2025 1:43:46 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[GeocodedIDs](
	[ID] [nvarchar](50) NOT NULL,
 CONSTRAINT [PK_GeocodedIDs] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Properties]    Script Date: 8/23/2025 1:43:46 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Properties](
	[PropertyId] [int] IDENTITY(1,1) NOT NULL,
	[SurveyPrimaryKey] [int] NOT NULL,
	[LegacyTax] [nvarchar](50) NULL,
	[District] [nvarchar](10) NULL,
	[Section] [nvarchar](10) NULL,
	[Block] [nvarchar](50) NULL,
	[Lot] [nvarchar](50) NULL,
	[AddressId] [int] NULL,
	[TownshipId] [int] NULL,
	[PropertyType] [nvarchar](50) NULL,
	[CreatedDate] [datetime2](7) NOT NULL,
	[ModifiedDate] [datetime2](7) NOT NULL,
 CONSTRAINT [PK__Properti__70C9A735A1D37F68] PRIMARY KEY CLUSTERED 
(
	[PropertyId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
 CONSTRAINT [UQ__Properti__9CF1543A16EB7292] UNIQUE NONCLUSTERED 
(
	[SurveyPrimaryKey] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Townships]    Script Date: 8/23/2025 1:43:46 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Townships](
	[TownshipId] [int] IDENTITY(1,1) NOT NULL,
	[Name] [nvarchar](100) NOT NULL,
	[FoilMethod] [nvarchar](255) NULL,
	[Website] [nvarchar](1000) NULL,
	[Description] [nvarchar](500) NULL,
 CONSTRAINT [PK_Townships] PRIMARY KEY CLUSTERED 
(
	[TownshipId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[SurveyDocuments]    Script Date: 8/23/2025 1:43:46 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SurveyDocuments](
	[DocumentId] [int] IDENTITY(1,1) NOT NULL,
	[SurveyId] [int] NOT NULL,
	[DocumentType] [nvarchar](50) NOT NULL,
	[FileName] [nvarchar](255) NOT NULL,
	[FilePath] [nvarchar](500) NOT NULL,
	[FileSize] [bigint] NULL,
	[MimeType] [nvarchar](100) NULL,
	[IsMainDocument] [bit] NOT NULL,
	[UploadedDate] [datetime2](7) NOT NULL,
	[UploadedBy] [nvarchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[DocumentId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[SurveyNotes]    Script Date: 8/23/2025 1:43:46 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SurveyNotes](
	[NoteId] [int] IDENTITY(1,1) NOT NULL,
	[SurveyId] [int] NOT NULL,
	[NoteType] [nvarchar](20) NOT NULL,
	[NoteText] [ntext] NOT NULL,
	[IsInternal] [bit] NOT NULL,
	[CreatedDate] [datetime2](7) NOT NULL,
	[CreatedBy] [nvarchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[NoteId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Surveys]    Script Date: 8/23/2025 1:43:46 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Surveys](
	[SurveyId] [int] NOT NULL,
	[SurveyNumber] [nvarchar](50) NOT NULL,
	[CustomerId] [int] NULL,
	[PropertyId] [int] NULL,
	[SurveyTypeId] [int] NULL,
	[StatusId] [int] NOT NULL,
	[Title] [nvarchar](255) NULL,
	[Description] [ntext] NULL,
	[PurposeCode] [nvarchar](50) NULL,
	[RequestDate] [datetime2](7) NULL,
	[ScheduledDate] [datetime2](7) NULL,
	[CompletedDate] [datetime2](7) NULL,
	[DeliveryDate] [datetime2](7) NULL,
	[DueDate] [datetime2](7) NULL,
	[QuotedPrice] [decimal](10, 2) NULL,
	[FinalPrice] [decimal](10, 2) NULL,
	[IsFieldworkComplete] [bit] NOT NULL,
	[IsDrawingComplete] [bit] NOT NULL,
	[IsScanned] [bit] NOT NULL,
	[IsDelivered] [bit] NOT NULL,
	[CreatedDate] [datetime2](7) NOT NULL,
	[ModifiedDate] [datetime2](7) NOT NULL,
	[CreatedBy] [nvarchar](100) NULL,
	[ModifiedBy] [nvarchar](100) NULL,
 CONSTRAINT [PK__Surveys__A5481F7D4AE5E3E8] PRIMARY KEY CLUSTERED 
(
	[SurveyId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[SurveyStatuses]    Script Date: 8/23/2025 1:43:46 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SurveyStatuses](
	[StatusId] [int] IDENTITY(1,1) NOT NULL,
	[StatusCode] [nvarchar](20) NOT NULL,
	[StatusName] [nvarchar](100) NOT NULL,
	[SortOrder] [int] NOT NULL,
	[IsActive] [bit] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[StatusId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[StatusCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[SurveyTypes]    Script Date: 8/23/2025 1:43:46 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SurveyTypes](
	[SurveyTypeId] [int] IDENTITY(1,1) NOT NULL,
	[TypeName] [nvarchar](100) NOT NULL,
	[TypeDescription] [nvarchar](500) NULL,
	[EstimatedDuration] [int] NULL,
	[BasePrice] [decimal](10, 2) NULL,
	[IsActive] [bit] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[SurveyTypeId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[TypeName] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ZIPCODES]    Script Date: 8/23/2025 1:43:46 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ZIPCODES](
	[Zip] [int] NULL,
	[Lat] [float] NULL,
	[Long] [float] NULL,
	[Town] [nvarchar](255) NULL,
	[State] [nvarchar](255) NULL,
	[County] [nvarchar](255) NULL,
	[Type] [nvarchar](255) NULL
) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [IX_Addresses_AddressLine1_City_Type]    Script Date: 8/23/2025 1:43:46 PM ******/
CREATE NONCLUSTERED INDEX [IX_Addresses_AddressLine1_City_Type] ON [dbo].[Addresses]
(
	[AddressLine1] ASC,
	[City] ASC,
	[AddressType] ASC
)
INCLUDE([AddressId]) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [IX_Addresses_TrimmedAddressJoin]    Script Date: 8/23/2025 1:43:46 PM ******/
CREATE NONCLUSTERED INDEX [IX_Addresses_TrimmedAddressJoin] ON [dbo].[Addresses]
(
	[AddressLine1] ASC,
	[City] ASC,
	[AddressType] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [NonClusteredIndex-20250812-201443]    Script Date: 8/23/2025 1:43:46 PM ******/
CREATE NONCLUSTERED INDEX [NonClusteredIndex-20250812-201443] ON [dbo].[Addresses]
(
	[AddressType] ASC,
	[AddressLine1] ASC,
	[City] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [IX_Customers_CompanyName]    Script Date: 8/23/2025 1:43:46 PM ******/
CREATE NONCLUSTERED INDEX [IX_Customers_CompanyName] ON [dbo].[Customers]
(
	[CompanyName] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [IX_Customers_Email]    Script Date: 8/23/2025 1:43:46 PM ******/
CREATE NONCLUSTERED INDEX [IX_Customers_Email] ON [dbo].[Customers]
(
	[Email] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IX_Properties_SurveyPrimaryKey]    Script Date: 8/23/2025 1:43:46 PM ******/
CREATE UNIQUE NONCLUSTERED INDEX [IX_Properties_SurveyPrimaryKey] ON [dbo].[Properties]
(
	[SurveyPrimaryKey] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IX_Properties_SurveyPrimaryKey_AddressId]    Script Date: 8/23/2025 1:43:46 PM ******/
CREATE NONCLUSTERED INDEX [IX_Properties_SurveyPrimaryKey_AddressId] ON [dbo].[Properties]
(
	[SurveyPrimaryKey] ASC
)
INCLUDE([AddressId]) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IX_Surveys_Customer]    Script Date: 8/23/2025 1:43:46 PM ******/
CREATE NONCLUSTERED INDEX [IX_Surveys_Customer] ON [dbo].[Surveys]
(
	[CustomerId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IX_Surveys_DueDate]    Script Date: 8/23/2025 1:43:46 PM ******/
CREATE NONCLUSTERED INDEX [IX_Surveys_DueDate] ON [dbo].[Surveys]
(
	[DueDate] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IX_Surveys_RequestDate]    Script Date: 8/23/2025 1:43:46 PM ******/
CREATE NONCLUSTERED INDEX [IX_Surveys_RequestDate] ON [dbo].[Surveys]
(
	[RequestDate] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IX_Surveys_Status]    Script Date: 8/23/2025 1:43:46 PM ******/
CREATE NONCLUSTERED INDEX [IX_Surveys_Status] ON [dbo].[Surveys]
(
	[StatusId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [IX_Surveys_SurveyNumber]    Script Date: 8/23/2025 1:43:46 PM ******/
CREATE NONCLUSTERED INDEX [IX_Surveys_SurveyNumber] ON [dbo].[Surveys]
(
	[SurveyNumber] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [IX_SurveyStatuses_StatusCode]    Script Date: 8/23/2025 1:43:46 PM ******/
CREATE UNIQUE NONCLUSTERED INDEX [IX_SurveyStatuses_StatusCode] ON [dbo].[SurveyStatuses]
(
	[StatusCode] ASC
)
INCLUDE([StatusId]) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Addresses] ADD  CONSTRAINT [DF__Addresses__Count__5070F446]  DEFAULT ('USA') FOR [Country]
GO
ALTER TABLE [dbo].[Addresses] ADD  CONSTRAINT [DF__Addresses__IsAct__5165187F]  DEFAULT ((1)) FOR [IsActive]
GO
ALTER TABLE [dbo].[Addresses] ADD  CONSTRAINT [DF__Addresses__Creat__52593CB8]  DEFAULT (getutcdate()) FOR [CreatedDate]
GO
ALTER TABLE [dbo].[CustomerAddresses] ADD  DEFAULT ((0)) FOR [IsPrimary]
GO
ALTER TABLE [dbo].[CustomerAddresses] ADD  DEFAULT (getutcdate()) FOR [CreatedDate]
GO
ALTER TABLE [dbo].[Customers] ADD  DEFAULT ((1)) FOR [IsActive]
GO
ALTER TABLE [dbo].[Customers] ADD  DEFAULT (getutcdate()) FOR [CreatedDate]
GO
ALTER TABLE [dbo].[Customers] ADD  DEFAULT (getutcdate()) FOR [ModifiedDate]
GO
ALTER TABLE [dbo].[Properties] ADD  CONSTRAINT [DF__Propertie__Creat__5BE2A6F2]  DEFAULT (getutcdate()) FOR [CreatedDate]
GO
ALTER TABLE [dbo].[Properties] ADD  CONSTRAINT [DF__Propertie__Modif__5CD6CB2B]  DEFAULT (getutcdate()) FOR [ModifiedDate]
GO
ALTER TABLE [dbo].[SurveyDocuments] ADD  DEFAULT ((0)) FOR [IsMainDocument]
GO
ALTER TABLE [dbo].[SurveyDocuments] ADD  DEFAULT (getutcdate()) FOR [UploadedDate]
GO
ALTER TABLE [dbo].[SurveyNotes] ADD  DEFAULT ((0)) FOR [IsInternal]
GO
ALTER TABLE [dbo].[SurveyNotes] ADD  DEFAULT (getutcdate()) FOR [CreatedDate]
GO
ALTER TABLE [dbo].[Surveys] ADD  CONSTRAINT [DF__Surveys__Request__6A30C649]  DEFAULT (getutcdate()) FOR [RequestDate]
GO
ALTER TABLE [dbo].[Surveys] ADD  CONSTRAINT [DF__Surveys__IsField__6B24EA82]  DEFAULT ((0)) FOR [IsFieldworkComplete]
GO
ALTER TABLE [dbo].[Surveys] ADD  CONSTRAINT [DF__Surveys__IsDrawi__6C190EBB]  DEFAULT ((0)) FOR [IsDrawingComplete]
GO
ALTER TABLE [dbo].[Surveys] ADD  CONSTRAINT [DF__Surveys__IsScann__6D0D32F4]  DEFAULT ((0)) FOR [IsScanned]
GO
ALTER TABLE [dbo].[Surveys] ADD  CONSTRAINT [DF__Surveys__IsDeliv__6E01572D]  DEFAULT ((0)) FOR [IsDelivered]
GO
ALTER TABLE [dbo].[Surveys] ADD  CONSTRAINT [DF__Surveys__Created__6EF57B66]  DEFAULT (getutcdate()) FOR [CreatedDate]
GO
ALTER TABLE [dbo].[Surveys] ADD  CONSTRAINT [DF__Surveys__Modifie__6FE99F9F]  DEFAULT (getutcdate()) FOR [ModifiedDate]
GO
ALTER TABLE [dbo].[SurveyStatuses] ADD  DEFAULT ((0)) FOR [SortOrder]
GO
ALTER TABLE [dbo].[SurveyStatuses] ADD  DEFAULT ((1)) FOR [IsActive]
GO
ALTER TABLE [dbo].[SurveyTypes] ADD  DEFAULT ((1)) FOR [IsActive]
GO
ALTER TABLE [dbo].[CustomerAddresses]  WITH CHECK ADD  CONSTRAINT [FK_CustomerAddresses_Address] FOREIGN KEY([AddressId])
REFERENCES [dbo].[Addresses] ([AddressId])
GO
ALTER TABLE [dbo].[CustomerAddresses] CHECK CONSTRAINT [FK_CustomerAddresses_Address]
GO
ALTER TABLE [dbo].[CustomerAddresses]  WITH CHECK ADD  CONSTRAINT [FK_CustomerAddresses_Customer] FOREIGN KEY([CustomerId])
REFERENCES [dbo].[Customers] ([CustomerId])
GO
ALTER TABLE [dbo].[CustomerAddresses] CHECK CONSTRAINT [FK_CustomerAddresses_Customer]
GO
ALTER TABLE [dbo].[Properties]  WITH CHECK ADD  CONSTRAINT [FK_Properties_Address] FOREIGN KEY([AddressId])
REFERENCES [dbo].[Addresses] ([AddressId])
GO
ALTER TABLE [dbo].[Properties] CHECK CONSTRAINT [FK_Properties_Address]
GO
ALTER TABLE [dbo].[SurveyDocuments]  WITH CHECK ADD  CONSTRAINT [FK_SurveyDocuments_Survey] FOREIGN KEY([SurveyId])
REFERENCES [dbo].[Surveys] ([SurveyId])
GO
ALTER TABLE [dbo].[SurveyDocuments] CHECK CONSTRAINT [FK_SurveyDocuments_Survey]
GO
ALTER TABLE [dbo].[SurveyNotes]  WITH CHECK ADD  CONSTRAINT [FK_SurveyNotes_Survey] FOREIGN KEY([SurveyId])
REFERENCES [dbo].[Surveys] ([SurveyId])
GO
ALTER TABLE [dbo].[SurveyNotes] CHECK CONSTRAINT [FK_SurveyNotes_Survey]
GO
ALTER TABLE [dbo].[Surveys]  WITH CHECK ADD  CONSTRAINT [FK_Surveys_Customer] FOREIGN KEY([CustomerId])
REFERENCES [dbo].[Customers] ([CustomerId])
GO
ALTER TABLE [dbo].[Surveys] CHECK CONSTRAINT [FK_Surveys_Customer]
GO
ALTER TABLE [dbo].[Surveys]  WITH CHECK ADD  CONSTRAINT [FK_Surveys_Property] FOREIGN KEY([PropertyId])
REFERENCES [dbo].[Properties] ([PropertyId])
GO
ALTER TABLE [dbo].[Surveys] CHECK CONSTRAINT [FK_Surveys_Property]
GO
ALTER TABLE [dbo].[Surveys]  WITH CHECK ADD  CONSTRAINT [FK_Surveys_Status] FOREIGN KEY([StatusId])
REFERENCES [dbo].[SurveyStatuses] ([StatusId])
GO
ALTER TABLE [dbo].[Surveys] CHECK CONSTRAINT [FK_Surveys_Status]
GO
ALTER TABLE [dbo].[Surveys]  WITH CHECK ADD  CONSTRAINT [FK_Surveys_SurveyType] FOREIGN KEY([SurveyTypeId])
REFERENCES [dbo].[SurveyTypes] ([SurveyTypeId])
GO
ALTER TABLE [dbo].[Surveys] CHECK CONSTRAINT [FK_Surveys_SurveyType]
GO
ALTER TABLE [dbo].[Properties]  WITH CHECK ADD  CONSTRAINT [FK_Properties_Township] FOREIGN KEY([TownshipId])
REFERENCES [dbo].[Townships] ([TownshipId])
GO
ALTER TABLE [dbo].[Properties] CHECK CONSTRAINT [FK_Properties_Township]
GO
