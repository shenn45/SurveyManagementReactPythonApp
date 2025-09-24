import { gql } from '@apollo/client';

// GraphQL queries for UserSettings
export const GET_USER_SETTINGS = gql`
  query GetUserSettings($settingsType: String!) {
    userSettings(settingsType: $settingsType) {
      UserSettingsId
      UserId
      SettingsType
      SettingsData
      IsActive
      CreatedDate
      ModifiedDate
    }
  }
`;

export const GET_ALL_USER_SETTINGS = gql`
  query GetAllUserSettings {
    allUserSettings {
      UserSettingsId
      UserId
      SettingsType
      SettingsData
      IsActive
      CreatedDate
      ModifiedDate
    }
  }
`;

// GraphQL mutation for UserSettings
export const UPSERT_USER_SETTINGS = gql`
  mutation UpsertUserSettings($input: UserSettingsInput!) {
    upsertUserSettings(input: $input) {
      userSettings {
        UserSettingsId
        UserId
        SettingsType
        SettingsData
        IsActive
        CreatedDate
        ModifiedDate
      }
    }
  }
`;