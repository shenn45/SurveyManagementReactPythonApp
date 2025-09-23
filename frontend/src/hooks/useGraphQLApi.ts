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
  GET_TOWNSHIPS,
  GET_TOWNSHIP,
  CREATE_TOWNSHIP,
  UPDATE_TOWNSHIP,
  DELETE_TOWNSHIP,
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
  TownshipListResponse
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
    return (result.data as any).createSurvey;
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
      refetchQueries: [GET_SURVEYS, GET_SURVEY],
    });
    return (result.data as any).updateSurvey;
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
  const { data, loading, error } = useQuery(GET_SURVEY_STATUSES);

  return {
    data: (data as any)?.surveyStatuses as SurveyStatus[] | undefined,
    loading,
    error,
  };
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
