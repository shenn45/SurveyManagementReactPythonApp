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
  Township
} from '../types';

// Customer hooks
export const useCustomers = (page = 1, size = 100, search?: string) => {
  const skip = (page - 1) * size;
  const { data, loading, error, refetch } = useQuery(GET_CUSTOMERS, {
    variables: { skip, limit: size, search },
  });

  return {
    data: data?.customers as CustomerListResponse | undefined,
    loading,
    error,
    refetch,
  };
};

export const useCustomer = (customerId: number) => {
  const { data, loading, error } = useQuery(GET_CUSTOMER, {
    variables: { customerId },
    skip: !customerId,
  });

  return {
    data: data?.customer as Customer | undefined,
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
    return result.data.createCustomer;
  };

  return { create, loading, error };
};

export const useUpdateCustomer = () => {
  const [updateCustomer, { loading, error }] = useMutation(UPDATE_CUSTOMER);

  const update = async (id: number, customer: Partial<CustomerCreate>): Promise<Customer> => {
    const result = await updateCustomer({
      variables: {
        customerId: id,
        input: customer,
      },
      refetchQueries: [GET_CUSTOMERS, GET_CUSTOMER],
    });
    return result.data.updateCustomer;
  };

  return { update, loading, error };
};

export const useDeleteCustomer = () => {
  const [deleteCustomer, { loading, error }] = useMutation(DELETE_CUSTOMER);

  const remove = async (id: number): Promise<boolean> => {
    const result = await deleteCustomer({
      variables: {
        customerId: id,
      },
      refetchQueries: [GET_CUSTOMERS],
    });
    return result.data.deleteCustomer;
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
    data: data?.surveys as SurveyListResponse | undefined,
    loading,
    error,
    refetch,
  };
};

export const useSurvey = (surveyId: number) => {
  const { data, loading, error } = useQuery(GET_SURVEY, {
    variables: { surveyId },
    skip: !surveyId,
  });

  return {
    data: data?.survey as Survey | undefined,
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
    return result.data.createSurvey;
  };

  return { create, loading, error };
};

export const useUpdateSurvey = () => {
  const [updateSurvey, { loading, error }] = useMutation(UPDATE_SURVEY);

  const update = async (id: number, survey: Partial<SurveyCreate>): Promise<Survey> => {
    const result = await updateSurvey({
      variables: {
        surveyId: id,
        input: survey,
      },
      refetchQueries: [GET_SURVEYS, GET_SURVEY],
    });
    return result.data.updateSurvey;
  };

  return { update, loading, error };
};

export const useDeleteSurvey = () => {
  const [deleteSurvey, { loading, error }] = useMutation(DELETE_SURVEY);

  const remove = async (id: number): Promise<boolean> => {
    const result = await deleteSurvey({
      variables: {
        surveyId: id,
      },
      refetchQueries: [GET_SURVEYS],
    });
    return result.data.deleteSurvey;
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
    data: data?.properties as PropertyListResponse | undefined,
    loading,
    error,
    refetch,
  };
};

export const useProperty = (propertyId: number) => {
  const { data, loading, error } = useQuery(GET_PROPERTY, {
    variables: { propertyId },
    skip: !propertyId,
  });

  return {
    data: data?.property as Property | undefined,
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
    return result.data.createProperty;
  };

  return { create, loading, error };
};

export const useUpdateProperty = () => {
  const [updateProperty, { loading, error }] = useMutation(UPDATE_PROPERTY);

  const update = async (id: number, property: Partial<PropertyCreate>): Promise<Property> => {
    const result = await updateProperty({
      variables: {
        propertyId: id,
        input: property,
      },
      refetchQueries: [GET_PROPERTIES, GET_PROPERTY],
    });
    return result.data.updateProperty;
  };

  return { update, loading, error };
};

export const useDeleteProperty = () => {
  const [deleteProperty, { loading, error }] = useMutation(DELETE_PROPERTY);

  const remove = async (id: number): Promise<boolean> => {
    const result = await deleteProperty({
      variables: {
        propertyId: id,
      },
      refetchQueries: [GET_PROPERTIES],
    });
    return result.data.deleteProperty;
  };

  return { remove, loading, error };
};

// Lookup hooks
export const useSurveyTypes = () => {
  const { data, loading, error } = useQuery(GET_SURVEY_TYPES);

  return {
    data: data?.surveyTypes as SurveyType[] | undefined,
    loading,
    error,
  };
};

export const useSurveyStatuses = () => {
  const { data, loading, error } = useQuery(GET_SURVEY_STATUSES);

  return {
    data: data?.surveyStatuses as SurveyStatus[] | undefined,
    loading,
    error,
  };
};

export const useTownships = () => {
  const { data, loading, error } = useQuery(GET_TOWNSHIPS);

  return {
    data: data?.townships as Township[] | undefined,
    loading,
    error,
  };
};
