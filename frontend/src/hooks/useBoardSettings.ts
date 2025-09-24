import { useState, useEffect, useCallback } from 'react';
import { useQuery, useMutation } from '@apollo/client/react';
import { GET_USER_SETTINGS, UPSERT_USER_SETTINGS } from '../graphql/userSettings';

// Board-specific settings interface
export interface BoardSettings {
  hiddenColumns: string[];
  columnOrder: string[];
}

// GraphQL response types
interface UserSettingsGraphQL {
  UserSettingsId: string;
  UserId: string;
  SettingsType: string;
  SettingsData: string;
  IsActive: boolean;
  CreatedDate: string;
  ModifiedDate: string;
}

interface GetUserSettingsData {
  userSettings: UserSettingsGraphQL | null;
}

export const useBoardSettings = () => {
  const [settings, setSettings] = useState<BoardSettings>({
    hiddenColumns: [],
    columnOrder: []
  });

  // GraphQL query to load settings
  const { data, loading, error, refetch } = useQuery<GetUserSettingsData>(GET_USER_SETTINGS, {
    variables: { settingsType: 'BoardSettings' },
    errorPolicy: 'all'
  });

  // Handle data loading and errors
  useEffect(() => {
    if (loading) return;

    if (error) {
      console.error('Error loading board settings:', error);
      
      // Fallback to localStorage if GraphQL fails
      try {
        const savedHiddenColumns = localStorage.getItem('boardHiddenColumns');
        const savedColumnOrder = localStorage.getItem('boardColumnOrder');
        
        setSettings({
          hiddenColumns: savedHiddenColumns ? JSON.parse(savedHiddenColumns) : [],
          columnOrder: savedColumnOrder ? JSON.parse(savedColumnOrder) : []
        });
      } catch (localError) {
        console.warn('Failed to load from localStorage:', localError);
        // Use defaults as final fallback
        setSettings({
          hiddenColumns: [],
          columnOrder: []
        });
      }
      return;
    }

    if (data?.userSettings?.SettingsData) {
      try {
        const boardSettings = JSON.parse(data.userSettings.SettingsData) as BoardSettings;
        setSettings({
          hiddenColumns: boardSettings.hiddenColumns || [],
          columnOrder: boardSettings.columnOrder || []
        });
      } catch (parseError) {
        console.warn('Failed to parse board settings:', parseError);
        // Use defaults on parse error
        setSettings({
          hiddenColumns: [],
          columnOrder: []
        });
      }
    } else {
      // No settings found, use defaults
      setSettings({
        hiddenColumns: [],
        columnOrder: []
      });
    }
  }, [data, loading, error]);

  // GraphQL mutation to save settings
  const [upsertUserSettings] = useMutation(UPSERT_USER_SETTINGS);

  // Save settings to database
  const saveSettings = useCallback(async (newSettings: Partial<BoardSettings>) => {
    try {
      const updatedSettings = { ...settings, ...newSettings };
      setSettings(updatedSettings);
      
      // Save to database via GraphQL
      await upsertUserSettings({
        variables: {
          input: {
            SettingsType: 'BoardSettings',
            SettingsData: JSON.stringify(updatedSettings)
          }
        }
      });
      
      // Also save to localStorage as backup
      try {
        localStorage.setItem('boardHiddenColumns', JSON.stringify(updatedSettings.hiddenColumns));
        localStorage.setItem('boardColumnOrder', JSON.stringify(updatedSettings.columnOrder));
      } catch (localError) {
        console.warn('Failed to save to localStorage:', localError);
      }
      
    } catch (err) {
      console.error('Error saving board settings:', err);
      
      // Revert the optimistic update
      setSettings(settings);
      
      // Try saving to localStorage as fallback
      try {
        const updatedSettings = { ...settings, ...newSettings };
        localStorage.setItem('boardHiddenColumns', JSON.stringify(updatedSettings.hiddenColumns));
        localStorage.setItem('boardColumnOrder', JSON.stringify(updatedSettings.columnOrder));
      } catch (localError) {
        console.warn('Failed to save to localStorage fallback:', localError);
      }
    }
  }, [settings, upsertUserSettings]);

  // Specific methods for common operations
  const updateHiddenColumns = useCallback((hiddenColumns: string[]) => {
    saveSettings({ hiddenColumns });
  }, [saveSettings]);

  const updateColumnOrder = useCallback((columnOrder: string[]) => {
    saveSettings({ columnOrder });
  }, [saveSettings]);

  const hideColumn = useCallback((columnId: string) => {
    const newHiddenColumns = [...settings.hiddenColumns];
    if (!newHiddenColumns.includes(columnId)) {
      newHiddenColumns.push(columnId);
      updateHiddenColumns(newHiddenColumns);
    }
  }, [settings.hiddenColumns, updateHiddenColumns]);

  const showColumn = useCallback((columnId: string) => {
    const newHiddenColumns = settings.hiddenColumns.filter(id => id !== columnId);
    updateHiddenColumns(newHiddenColumns);
  }, [settings.hiddenColumns, updateHiddenColumns]);

  const showAllColumns = useCallback(() => {
    updateHiddenColumns([]);
  }, [updateHiddenColumns]);

  return {
    settings,
    isLoading: loading,
    error: error?.message || null,
    updateHiddenColumns,
    updateColumnOrder,
    hideColumn,
    showColumn,
    showAllColumns,
    saveSettings,
    reloadSettings: refetch
  };
};