# DefaultApi

All URIs are relative to *https://api.cumaker.space*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**equipmentGet**](DefaultApi.md#equipmentGet) | **GET** /equipment | Retrieve all equipment usage data |
| [**equipmentPost**](DefaultApi.md#equipmentPost) | **POST** /equipment | Create a new equipment usage data entry. Fails on existing UserID and Timestamp |
| [**equipmentUserIdGet**](DefaultApi.md#equipmentUserIdGet) | **GET** /equipment/{user_id} | Retrieve all equipment usage data for a specific user. |
| [**equipmentUserIdPatch**](DefaultApi.md#equipmentUserIdPatch) | **PATCH** /equipment/{user_id} | Update data in an existing equipment usage data entry. Specify the timestamp field to get a specific entry, or leave it blank to get the data entry with the latest timestamp. |
| [**qualificationsGet**](DefaultApi.md#qualificationsGet) | **GET** /qualifications | Retrieve all qualification data |
| [**qualificationsPost**](DefaultApi.md#qualificationsPost) | **POST** /qualifications | Create a new qualification entry for a user. Fails on existing UserID |
| [**qualificationsUserIdGet**](DefaultApi.md#qualificationsUserIdGet) | **GET** /qualifications/{user_id} | Retrieve qualification data for a specific user |
| [**qualificationsUserIdPatch**](DefaultApi.md#qualificationsUserIdPatch) | **PATCH** /qualifications/{user_id} | Update a qualification entry for a user. Unique items included in any completable item field are appended to that field. Any duplicate completable item is disregarded within that given field. |
| [**usersGet**](DefaultApi.md#usersGet) | **GET** /users | Retrieve all user data |
| [**usersPost**](DefaultApi.md#usersPost) | **POST** /users | Create a new user. Fails on existing UserID |
| [**usersUserIdGet**](DefaultApi.md#usersUserIdGet) | **GET** /users/{user_id} | Retrieve user data for a specific user |
| [**usersUserIdPatch**](DefaultApi.md#usersUserIdPatch) | **PATCH** /users/{user_id} | Update data for an existing user |
| [**visitsGet**](DefaultApi.md#visitsGet) | **GET** /visits | Retrieve all visit data |
| [**visitsPost**](DefaultApi.md#visitsPost) | **POST** /visits | Create a new visit entry. Fails on existing UserID and Timestamp |
| [**visitsUserIdGet**](DefaultApi.md#visitsUserIdGet) | **GET** /visits/{user_id} | Retrieve all visits for a specific user |


<a name="equipmentGet"></a>
# **equipmentGet**
> EquipmentUsages equipmentGet(start\_timestamp, end\_timestamp, limit)

Retrieve all equipment usage data

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **start\_timestamp** | **Date**| Used to query for results with timestamps greater than or equal to start_timestamp. If used alongside end_timestamp, it MUST be less than or equal to it. | [optional] [default to null] |
| **end\_timestamp** | **Date**| Used to query for results with timestamps less than or equal to end_timestamp. If used alongside start_timestamp, it MUST be greater than or equal to it. | [optional] [default to null] |
| **limit** | **Integer**| The maximum number of results to return from a table scan/query. | [optional] [default to null] |

### Return type

[**EquipmentUsages**](../Models/EquipmentUsages.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="equipmentPost"></a>
# **equipmentPost**
> equipmentPost(EquipmentUsage)

Create a new equipment usage data entry. Fails on existing UserID and Timestamp

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **EquipmentUsage** | [**EquipmentUsage**](../Models/EquipmentUsage.md)| Create a new equipment usage table entry. | [optional] |

### Return type

null (empty response body)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="equipmentUserIdGet"></a>
# **equipmentUserIdGet**
> EquipmentUsages equipmentUserIdGet(user\_id, start\_timestamp, end\_timestamp, limit)

Retrieve all equipment usage data for a specific user.

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **user\_id** | [**UserID**](../Models/.md)|  | [default to null] |
| **start\_timestamp** | **Date**| Used to query for results with timestamps greater than or equal to start_timestamp. If used alongside end_timestamp, it MUST be less than or equal to it. | [optional] [default to null] |
| **end\_timestamp** | **Date**| Used to query for results with timestamps less than or equal to end_timestamp. If used alongside start_timestamp, it MUST be greater than or equal to it. | [optional] [default to null] |
| **limit** | **Integer**| The maximum number of results to return from a table scan/query. | [optional] [default to null] |

### Return type

[**EquipmentUsages**](../Models/EquipmentUsages.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="equipmentUserIdPatch"></a>
# **equipmentUserIdPatch**
> equipmentUserIdPatch(user\_id, EquipmentUsageProperties)

Update data in an existing equipment usage data entry. Specify the timestamp field to get a specific entry, or leave it blank to get the data entry with the latest timestamp.

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **user\_id** | [**UserID**](../Models/.md)|  | [default to null] |
| **EquipmentUsageProperties** | [**EquipmentUsageProperties**](../Models/EquipmentUsageProperties.md)| Update an equipment usage entry. Changed fields are required to exhibit any documented required field sets (e.g., changing equipment_type from \&quot;Laser Engraver\&quot;-&gt;\&quot;3D Printer\&quot; means a 3d_printer_info object must be provided in the request body). The user_id and timestamp fields will NEVER be changed, even if they are provided in the request body. If the timestamp field is not provided, the latest entry in the equipment usage table for the user will be updated instead. | [optional] |

### Return type

null (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="qualificationsGet"></a>
# **qualificationsGet**
> Qualifications qualificationsGet(start\_timestamp, end\_timestamp, limit)

Retrieve all qualification data

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **start\_timestamp** | **Date**| Used to query for results with timestamps greater than or equal to start_timestamp. If used alongside end_timestamp, it MUST be less than or equal to it. | [optional] [default to null] |
| **end\_timestamp** | **Date**| Used to query for results with timestamps less than or equal to end_timestamp. If used alongside start_timestamp, it MUST be greater than or equal to it. | [optional] [default to null] |
| **limit** | **Integer**| The maximum number of results to return from a table scan/query. | [optional] [default to null] |

### Return type

[**Qualifications**](../Models/Qualifications.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="qualificationsPost"></a>
# **qualificationsPost**
> qualificationsPost(Qualification)

Create a new qualification entry for a user. Fails on existing UserID

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **Qualification** | [**Qualification**](../Models/Qualification.md)| Create a new qualifications table entry. The last_updated field will always be managed by the server, and will never change to a value provided in a request body. | [optional] |

### Return type

null (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="qualificationsUserIdGet"></a>
# **qualificationsUserIdGet**
> Qualification qualificationsUserIdGet(user\_id)

Retrieve qualification data for a specific user

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **user\_id** | [**UserID**](../Models/.md)|  | [default to null] |

### Return type

[**Qualification**](../Models/Qualification.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="qualificationsUserIdPatch"></a>
# **qualificationsUserIdPatch**
> qualificationsUserIdPatch(user\_id, QualificationsProperties)

Update a qualification entry for a user. Unique items included in any completable item field are appended to that field. Any duplicate completable item is disregarded within that given field.

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **user\_id** | [**UserID**](../Models/.md)|  | [default to null] |
| **QualificationsProperties** | [**QualificationsProperties**](../Models/QualificationsProperties.md)| Update a qualifications entry. It is required when updating any object that is an array of completable items that the request array contains all existing keys. Changed values of existing keys and any new key:value pairs will be added. The user_id field will NEVER be changed, even if it is provided in the request body. The last_updated field will always be managed by the server, and will never change to a value provided in a request body. | [optional] |

### Return type

null (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="usersGet"></a>
# **usersGet**
> Users usersGet(limit)

Retrieve all user data

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **limit** | **Integer**| The maximum number of results to return from a table scan/query. | [optional] [default to null] |

### Return type

[**Users**](../Models/Users.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="usersPost"></a>
# **usersPost**
> usersPost(User)

Create a new user. Fails on existing UserID

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **User** | [**User**](../Models/User.md)| Create a new user information table entry. | [optional] |

### Return type

null (empty response body)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="usersUserIdGet"></a>
# **usersUserIdGet**
> User usersUserIdGet(user\_id)

Retrieve user data for a specific user

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **user\_id** | [**UserID**](../Models/.md)|  | [default to null] |

### Return type

[**User**](../Models/User.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="usersUserIdPatch"></a>
# **usersUserIdPatch**
> usersUserIdPatch(user\_id, UserProperties)

Update data for an existing user

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **user\_id** | [**UserID**](../Models/.md)|  | [default to null] |
| **UserProperties** | [**UserProperties**](../Models/UserProperties.md)| Update an equipment usage entry. Changed fields are required to exhibit any documented required field sets (e.g., changing university_status from Employee-&gt;Undergraduate means the major and undergraduate_class must be defined in the request body). The user_id field will NEVER be changed, even if it is provided in the request body. | [optional] |

### Return type

null (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="visitsGet"></a>
# **visitsGet**
> Visits visitsGet(start\_timestamp, end\_timestamp, limit)

Retrieve all visit data

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **start\_timestamp** | **Date**| Used to query for results with timestamps greater than or equal to start_timestamp. If used alongside end_timestamp, it MUST be less than or equal to it. | [optional] [default to null] |
| **end\_timestamp** | **Date**| Used to query for results with timestamps less than or equal to end_timestamp. If used alongside start_timestamp, it MUST be greater than or equal to it. | [optional] [default to null] |
| **limit** | **Integer**| The maximum number of results to return from a table scan/query. | [optional] [default to null] |

### Return type

[**Visits**](../Models/Visits.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="visitsPost"></a>
# **visitsPost**
> visitsPost(Visit)

Create a new visit entry. Fails on existing UserID and Timestamp

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **Visit** | [**Visit**](../Models/Visit.md)| Create a new visit table entry. | [optional] |

### Return type

null (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

<a name="visitsUserIdGet"></a>
# **visitsUserIdGet**
> Visits visitsUserIdGet(user\_id, start\_timestamp, end\_timestamp, limit)

Retrieve all visits for a specific user

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **user\_id** | [**UserID**](../Models/.md)|  | [default to null] |
| **start\_timestamp** | **Date**| Used to query for results with timestamps greater than or equal to start_timestamp. If used alongside end_timestamp, it MUST be less than or equal to it. | [optional] [default to null] |
| **end\_timestamp** | **Date**| Used to query for results with timestamps less than or equal to end_timestamp. If used alongside start_timestamp, it MUST be greater than or equal to it. | [optional] [default to null] |
| **limit** | **Integer**| The maximum number of results to return from a table scan/query. | [optional] [default to null] |

### Return type

[**Visits**](../Models/Visits.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

