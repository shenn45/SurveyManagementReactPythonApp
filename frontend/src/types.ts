export interface Customer {
  CustomerId: string;
  CustomerCode: string;
  CompanyName: string;
  ContactFirstName?: string;
  ContactLastName?: string;
  Email?: string;
  Phone?: string;
  Fax?: string;
  Website?: string;
  IsActive: boolean;
  CreatedDate: string;
  ModifiedDate: string;
  CreatedBy?: string;
  ModifiedBy?: string;
}

export interface CustomerCreate {
  CustomerCode: string;
  CompanyName: string;
  ContactFirstName?: string;
  ContactLastName?: string;
  Email?: string;
  Phone?: string;
  Fax?: string;
  Website?: string;
  IsActive?: boolean;
}

export interface Survey {
  SurveyId: string;
  SurveyNumber: string;
  CustomerId?: string;
  PropertyId?: string;
  SurveyTypeId?: string;
  StatusId?: string;
  Title?: string;
  Description?: string;
  PurposeCode?: string;
  RequestDate?: string;
  ScheduledDate?: string;
  CompletedDate?: string;
  DeliveryDate?: string;
  DueDate?: string;
  QuotedPrice?: number;
  FinalPrice?: number;
  IsFieldworkComplete: boolean;
  IsDrawingComplete: boolean;
  IsScanned: boolean;
  IsDelivered: boolean;
  CreatedDate: string;
  ModifiedDate: string;
  CreatedBy?: string;
  ModifiedBy?: string;
  customer?: Customer;
  property?: Property;
  survey_type?: SurveyType;
  status?: SurveyStatus;
  notes: SurveyNote[];
  documents: SurveyDocument[];
}

export interface SurveyCreate {
  SurveyNumber: string;
  CustomerId?: string;
  PropertyId?: string;
  SurveyTypeId?: string;
  StatusId?: string;
  Title?: string;
  Description?: string;
  PurposeCode?: string;
  RequestDate?: string;
  ScheduledDate?: string;
  CompletedDate?: string;
  DeliveryDate?: string;
  DueDate?: string;
  QuotedPrice?: number;
  FinalPrice?: number;
  IsFieldworkComplete?: boolean;
  IsDrawingComplete?: boolean;
  IsScanned?: boolean;
  IsDelivered?: boolean;
}

export interface Property {
  PropertyId: string;
  PropertyCode: string;
  PropertyName: string;
  PropertyDescription?: string;
  OwnerName?: string;
  OwnerPhone?: string;
  OwnerEmail?: string;
  AddressId?: string;
  TownshipId?: string;
  IsActive: boolean;
  CreatedDate: string;
  ModifiedDate: string;
  CreatedBy?: string;
  ModifiedBy?: string;
  // Legacy fields for backward compatibility
  SurveyPrimaryKey?: number;
  LegacyTax?: string;
  District?: string;
  Section?: string;
  Block?: string;
  Lot?: string;
  PropertyType?: string;
  address?: Address;
  township?: Township;
}

export interface PropertyCreate {
  PropertyCode: string;
  PropertyName: string;
  PropertyDescription?: string;
  OwnerName?: string;
  OwnerPhone?: string;
  OwnerEmail?: string;
  AddressId?: string;
  TownshipId?: string;
  IsActive?: boolean;
  // Legacy fields for backward compatibility
  SurveyPrimaryKey?: number;
  LegacyTax?: string;
  District?: string;
  Section?: string;
  Block?: string;
  Lot?: string;
  PropertyType?: string;
}

export interface Address {
  AddressId: number;
  AddressType: string;
  AddressLine1: string;
  AddressLine2?: string;
  City: string;
  StateCode: string;
  ZipCode: string;
  County?: string;
  Country?: string;
  IsActive: boolean;
  CreatedDate: string;
}

export interface SurveyType {
  SurveyTypeId: string;
  SurveyTypeName: string;
  Description?: string;
  IsActive: boolean;
}

export interface SurveyStatus {
  SurveyStatusId: string;
  StatusName: string;
  Description?: string;
  IsActive: boolean;
}

export interface Township {
  TownshipId: string;
  TownshipName: string;
  County: string;
  State: string;
  IsActive: boolean;
  CreatedDate: string;
  ModifiedDate: string;
  CreatedBy?: string;
  ModifiedBy?: string;
}

export interface TownshipCreate {
  TownshipName: string;
  County: string;
  State: string;
  IsActive?: boolean;
}

export interface SurveyNote {
  NoteId: number;
  SurveyId: number;
  NoteType: string;
  NoteText: string;
  IsInternal: boolean;
  CreatedDate: string;
  CreatedBy?: string;
}

export interface SurveyDocument {
  DocumentId: number;
  SurveyId: number;
  DocumentType: string;
  FileName: string;
  FilePath: string;
  FileSize?: number;
  MimeType?: string;
  IsMainDocument: boolean;
  UploadedDate: string;
  UploadedBy?: string;
}

export interface PaginatedResponse<T> {
  total: number;
  page: number;
  size: number;
  data?: T[];
}

export interface CustomerListResponse extends PaginatedResponse<Customer> {
  customers: Customer[];
}

export interface SurveyListResponse extends PaginatedResponse<Survey> {
  surveys: Survey[];
}

export interface PropertyListResponse extends PaginatedResponse<Property> {
  properties: Property[];
}

export interface TownshipListResponse extends PaginatedResponse<Township> {
  townships: Township[];
}

export interface UserSettings {
  UserSettingsId: string;
  UserId: string;
  SettingsType: string;
  SettingsData: Record<string, any>;
  IsActive: boolean;
  CreatedDate: string;
  ModifiedDate: string;
}

export interface UserSettingsCreate {
  UserId: string;
  SettingsType: string;
  SettingsData: Record<string, any>;
  IsActive?: boolean;
}

export interface UserSettingsUpdate {
  SettingsData?: Record<string, any>;
  IsActive?: boolean;
}

export interface BoardConfiguration {
  BoardConfigId: string;
  BoardName: string;
  BoardSlug: string;
  Description?: string;
  UserId?: string;
  IsDefault: boolean;
  IsActive: boolean;
  CreatedDate: string;
  ModifiedDate: string;
  CreatedBy?: string;
  ModifiedBy?: string;
}

export interface BoardConfigurationCreate {
  BoardName: string;
  Description?: string;
  UserId?: string;
  IsDefault?: boolean;
  IsActive?: boolean;
}

export interface BoardConfigurationUpdate {
  BoardName?: string;
  BoardSlug?: string;
  Description?: string;
  IsDefault?: boolean;
  IsActive?: boolean;
}

export interface BoardConfigurationListResponse extends PaginatedResponse<BoardConfiguration> {
  board_configurations: BoardConfiguration[];
}
