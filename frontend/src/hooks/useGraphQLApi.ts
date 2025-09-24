import { useQuery, useMutation } from '@apollo/client/react';
import {
  GET_CUSTOMERS,
  GET_CUSTOMER,
  CREATE_CUSTOMER,
  UPDATE_CUSTOMER,
  DELETE_CUSTOMER,
  GET_SURVEYS,
  GET_SURVEY,
  CREATE_SURVEY,
  UPDATE_SURVEY,
  DELETE_SURVEY,
  GET_PROPERTIES,
  GET_PROPERTY,
  CREATE_PROPERTY,
  UPDATE_PROPERTY,
  DELETE_PROPERTY,
  GET_SURVEY_TYPES,
  GET_SURVEY_STATUSES,
  CREATE_SURVEY_STATUS,
  UPDATE_SURVEY_STATUS,
  GET_TOWNSHIPS,
  GET_TOWNSHIP,
  CREATE_TOWNSHIP,
  UPDATE_TOWNSHIP,
  DELETE_TOWNSHIP,
  GET_BOARD_CONFIGURATIONS,
  GET_BOARD_CONFIGURATION,
  GET_BOARD_CONFIGURATION_BY_SLUG,
  GET_DEFAULT_BOARD_CONFIGURATION,
  CREATE_BOARD_CONFIGURATION,
  UPDATE_BOARD_CONFIGURATION,
  DELETE_BOARD_CONFIGURATION,
} from '../graphql/queries';

import {
  Customer,
  CustomerCreate,
  CustomerListResponse,
  Survey,
  SurveyCreate,
  SurveyListResponse,
  Property,
  PropertyCreate,
  PropertyListResponse,
  SurveyType,
  SurveyStatus,
  Township,
  TownshipCreate,
  TownshipListResponse,
  BoardConfiguration,
  BoardConfigurationCreate,
  BoardConfigurationUpdate
} from '../types';

// Customer hooks
export const useCustomers = (page = 1, size = 100, search?: string) => {
  const skip = (page - 1) * size;
  const { data, loading, error, refetch } = useQuery(GET_CUSTOMERS, {
    variables: { skip, limit: size, search },
  });

  return {
    data: (data as any)?.customers as CustomerListResponse | undefined,
    loading,
    error,
    refetch,
  };
};

export const useCustomer = (customerId: string) => {
  const { data, loading, error } = useQuery(GET_CUSTOMER, {
    variables: { customerId },
    skip: !customerId,
  });

  return {
    data: (data as any)?.customer as Customer | undefined,
    loading,
    error,
  };
};

export const useCreateCustomer = () => {
  const [createCustomer, { loading, error }] = useMutation(CREATE_CUSTOMER);

  const create = async (customer: CustomerCreate): Promise<Customer> => {
    const result = await createCustomer({
      variables: {
        input: customer,
      },
      refetchQueries: [GET_CUSTOMERS],
    });
    return (result.data as any).createCustomer.customer;
  };

  return { create, loading, error };
};

export const useUpdateCustomer = () => {
  const [updateCustomer, { loading, error }] = useMutation(UPDATE_CUSTOMER);

  const update = async (id: string, customer: Partial<CustomerCreate>): Promise<Customer> => {
    const result = await updateCustomer({
      variables: {
        customerId: id,
        input: customer,
      },
      refetchQueries: [GET_CUSTOMERS, GET_CUSTOMER],
    });
    return (result.data as any).updateCustomer.customer;
  };

  return { update, loading, error };
};

export const useDeleteCustomer = () => {
  const [deleteCustomer, { loading, error }] = useMutation(DELETE_CUSTOMER);

  const remove = async (id: string): Promise<boolean> => {
    const result = await deleteCustomer({
      variables: {
        customerId: id,
      },
      refetchQueries: [GET_CUSTOMERS],
    });
    return (result.data as any).deleteCustomer.success;
  };

  return { remove, loading, error };
};

// Survey hooks
export const useSurveys = (page = 1, size = 100, search?: string) => {
  const skip = (page - 1) * size;
  const { data, loading, error, refetch } = useQuery(GET_SURVEYS, {
    variables: { skip, limit: size, search },
  });

  return {
    data: (data as any)?.surveys as SurveyListResponse | undefined,
    loading,
    error,
    refetch,
  };
};

export const useSurvey = (surveyId: string) => {
  const { data, loading, error } = useQuery(GET_SURVEY, {
    variables: { surveyId },
    skip: !surveyId,
  });

  return {
    data: (data as any)?.survey as Survey | undefined,
    loading,
    error,
  };
};

export const useCreateSurvey = () => {
  const [createSurvey, { loading, error }] = useMutation(CREATE_SURVEY);

  const create = async (survey: SurveyCreate): Promise<Survey> => {
    const result = await createSurvey({
      variables: {
        input: survey,
      },
      refetchQueries: [GET_SURVEYS],
    });
    return (result.data as any).createSurvey.survey;
  };

  return { create, loading, error };
};

export const useUpdateSurvey = () => {
  const [updateSurvey, { loading, error }] = useMutation(UPDATE_SURVEY);

  const update = async (id: string, survey: Partial<SurveyCreate>): Promise<Survey> => {
    const result = await updateSurvey({
      variables: {
        surveyId: id,
        input: survey,
      },
      // Remove automatic refetch to prevent page reloads
      // refetchQueries: [GET_SURVEYS, GET_SURVEY],
    });
    return (result.data as any).updateSurvey.survey;
  };

  return { update, loading, error };
};

export const useDeleteSurvey = () => {
  const [deleteSurvey, { loading, error }] = useMutation(DELETE_SURVEY);

  const remove = async (id: string): Promise<boolean> => {
    const result = await deleteSurvey({
      variables: {
        surveyId: id,
      },
      refetchQueries: [GET_SURVEYS],
    });
    return (result.data as any).deleteSurvey;
  };

  return { remove, loading, error };
};

// Property hooks
export const useProperties = (page = 1, size = 100, search?: string) => {
  const skip = (page - 1) * size;
  const { data, loading, error, refetch } = useQuery(GET_PROPERTIES, {
    variables: { skip, limit: size, search },
  });

  return {
    data: (data as any)?.properties as PropertyListResponse | undefined,
    loading,
    error,
    refetch,
  };
};

export const useProperty = (propertyId: string) => {
  const { data, loading, error } = useQuery(GET_PROPERTY, {
    variables: { propertyId },
    skip: !propertyId,
  });

  return {
    data: (data as any)?.property as Property | undefined,
    loading,
    error,
  };
};

export const useCreateProperty = () => {
  const [createProperty, { loading, error }] = useMutation(CREATE_PROPERTY);

  const create = async (property: PropertyCreate): Promise<Property> => {
    const result = await createProperty({
      variables: {
        input: property,
      },
      refetchQueries: [GET_PROPERTIES],
    });
    return (result.data as any).createProperty.property;
  };

  return { create, loading, error };
};

export const useUpdateProperty = () => {
  const [updateProperty, { loading, error }] = useMutation(UPDATE_PROPERTY);

  const update = async (id: string, property: Partial<PropertyCreate>): Promise<Property> => {
    const result = await updateProperty({
      variables: {
        propertyId: id,
        input: property,
      },
      refetchQueries: [GET_PROPERTIES, GET_PROPERTY],
    });
    return (result.data as any).updateProperty.property;
  };

  return { update, loading, error };
};

export const useDeleteProperty = () => {
  const [deleteProperty, { loading, error }] = useMutation(DELETE_PROPERTY);

  const remove = async (id: string): Promise<boolean> => {
    const result = await deleteProperty({
      variables: {
        propertyId: id,
      },
      refetchQueries: [GET_PROPERTIES],
    });
    return (result.data as any).deleteProperty.success;
  };

  return { remove, loading, error };
};

// Lookup hooks
export const useSurveyTypes = () => {
  const { data, loading, error } = useQuery(GET_SURVEY_TYPES);

  return {
    data: (data as any)?.surveyTypes as SurveyType[] | undefined,
    loading,
    error,
  };
};

export const useSurveyStatuses = () => {
  const { data, loading, error, refetch } = useQuery(GET_SURVEY_STATUSES);

  return {
    data: (data as any)?.surveyStatuses as SurveyStatus[] | undefined,
    loading,
    error,
    refetch,
  };
};

export const useCreateSurveyStatus = () => {
  const [createSurveyStatus, { loading, error }] = useMutation(CREATE_SURVEY_STATUS);

  const create = async (input: { StatusName: string; Description?: string; IsActive?: boolean }): Promise<SurveyStatus> => {
    const result = await createSurveyStatus({
      variables: { input },
      refetchQueries: [GET_SURVEY_STATUSES],
    });
    return (result.data as any).createSurveyStatus.surveyStatus;
  };

  return { create, loading, error };
};

export const useUpdateSurveyStatus = () => {
  const [updateSurveyStatus, { loading, error }] = useMutation(UPDATE_SURVEY_STATUS);

  const update = async (surveyStatusId: string, input: { StatusName?: string; Description?: string; IsActive?: boolean }): Promise<SurveyStatus> => {
    const result = await updateSurveyStatus({
      variables: { surveyStatusId, input },
      refetchQueries: [GET_SURVEY_STATUSES],
    });
    return (result.data as any).updateSurveyStatus.surveyStatus;
  };

  return { update, loading, error };
};

export const useTownships = (page = 1, size = 100, search?: string) => {
  const skip = (page - 1) * size;
  const { data, loading, error, refetch } = useQuery(GET_TOWNSHIPS, {
    variables: { skip, limit: size, search },
  });

  return {
    data: (data as any)?.townships as TownshipListResponse | undefined,
    loading,
    error,
    refetch,
  };
};

export const useTownship = (townshipId: string) => {
  const { data, loading, error } = useQuery(GET_TOWNSHIP, {
    variables: { townshipId },
    skip: !townshipId,
  });

  return {
    data: (data as any)?.township as Township | undefined,
    loading,
    error,
  };
};

export const useCreateTownship = () => {
  const [createTownship, { loading, error }] = useMutation(CREATE_TOWNSHIP);

  const create = async (township: TownshipCreate): Promise<Township> => {
    const result = await createTownship({
      variables: {
        input: township,
      },
      refetchQueries: [GET_TOWNSHIPS],
    });
    return (result.data as any).createTownship.township;
  };

  return { create, loading, error };
};

export const useUpdateTownship = () => {
  const [updateTownship, { loading, error }] = useMutation(UPDATE_TOWNSHIP);

  const update = async (id: string, township: Partial<TownshipCreate>): Promise<Township> => {
    const result = await updateTownship({
      variables: {
        townshipId: id,
        input: township,
      },
      refetchQueries: [GET_TOWNSHIPS, GET_TOWNSHIP],
    });
    return (result.data as any).updateTownship.township;
  };

  return { update, loading, error };
};

export const useDeleteTownship = () => {
  const [deleteTownship, { loading, error }] = useMutation(DELETE_TOWNSHIP);

  const remove = async (id: string): Promise<boolean> => {
    const result = await deleteTownship({
      variables: {
        townshipId: id,
      },
      refetchQueries: [GET_TOWNSHIPS],
    });
    return (result.data as any).deleteTownship.success;
  };

  return { remove, loading, error };
};

// Board Configuration hooks
export const useBoardConfigurations = () => {
  const { data, loading, error, refetch } = useQuery(GET_BOARD_CONFIGURATIONS);

  return {
    data: (data as any)?.boardConfigurations as BoardConfiguration[] | undefined,
    loading,
    error,
    refetch,
  };
};

export const useBoardConfiguration = (boardConfigId: string) => {
  const { data, loading, error } = useQuery(GET_BOARD_CONFIGURATION, {
    variables: { boardConfigId },
    skip: !boardConfigId,
  });

  return {
    data: (data as any)?.boardConfiguration as BoardConfiguration | undefined,
    loading,
    error,
  };
};

export const useBoardConfigurationBySlug = (boardSlug: string) => {
  const { data, loading, error, refetch } = useQuery(GET_BOARD_CONFIGURATION_BY_SLUG, {
    variables: { boardSlug },
    skip: !boardSlug,
  });

  return {
    data: (data as any)?.boardConfigurationBySlug as BoardConfiguration | undefined,
    loading,
    error,
    refetch,
  };
};

export const useDefaultBoardConfiguration = () => {
  const { data, loading, error, refetch } = useQuery(GET_DEFAULT_BOARD_CONFIGURATION);

  return {
    data: (data as any)?.defaultBoardConfiguration as BoardConfiguration | undefined,
    loading,
    error,
    refetch,
  };
};

export const useCreateBoardConfiguration = () => {
  const [createBoardConfiguration, { loading, error }] = useMutation(CREATE_BOARD_CONFIGURATION);

  const create = async (boardConfig: BoardConfigurationCreate): Promise<BoardConfiguration> => {
    const result = await createBoardConfiguration({
      variables: {
        boardConfig,
      },
      refetchQueries: [GET_BOARD_CONFIGURATIONS, GET_DEFAULT_BOARD_CONFIGURATION],
    });
    return (result.data as any).createBoardConfiguration.boardConfiguration;
  };

  return { create, loading, error };
};

export const useUpdateBoardConfiguration = () => {
  const [updateBoardConfiguration, { loading, error }] = useMutation(UPDATE_BOARD_CONFIGURATION);

  const update = async (id: string, boardConfig: BoardConfigurationUpdate): Promise<BoardConfiguration> => {
    const result = await updateBoardConfiguration({
      variables: {
        boardConfigId: id,
        boardConfig,
      },
      refetchQueries: [GET_BOARD_CONFIGURATIONS, GET_BOARD_CONFIGURATION, GET_DEFAULT_BOARD_CONFIGURATION],
    });
    return (result.data as any).updateBoardConfiguration.boardConfiguration;
  };

  return { update, loading, error };
};

export const useDeleteBoardConfiguration = () => {
  const [deleteBoardConfiguration, { loading, error }] = useMutation(DELETE_BOARD_CONFIGURATION);

  const remove = async (id: string): Promise<boolean> => {
    const result = await deleteBoardConfiguration({
      variables: {
        boardConfigId: id,
      },
      refetchQueries: [GET_BOARD_CONFIGURATIONS, GET_DEFAULT_BOARD_CONFIGURATION],
    });
    return (result.data as any).deleteBoardConfiguration.success;
  };

  return { remove, loading, error };
};
