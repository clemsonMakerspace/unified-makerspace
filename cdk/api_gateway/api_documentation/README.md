# Documentation for User Management and Data Tracking API

<a name="documentation-for-api-endpoints"></a>
## Documentation for API Endpoints

All URIs are relative to *https://api.cumaker.space*

| Class | Method | HTTP request | Description |
|------------ | ------------- | ------------- | -------------|
| *DefaultApi* | [**equipmentGet**](Apis/DefaultApi.md#equipmentget) | **GET** /equipment | Retrieve all equipment usage data |
*DefaultApi* | [**equipmentPost**](Apis/DefaultApi.md#equipmentpost) | **POST** /equipment | Create a new equipment usage data entry. Fails on existing UserID and Timestamp |
*DefaultApi* | [**equipmentUserIdGet**](Apis/DefaultApi.md#equipmentuseridget) | **GET** /equipment/{user_id} | Retrieve all equipment usage data for a specific user. |
*DefaultApi* | [**equipmentUserIdPatch**](Apis/DefaultApi.md#equipmentuseridpatch) | **PATCH** /equipment/{user_id} | Update data in an existing equipment usage data entry. Specify the timestamp field to get a specific entry, or leave it blank to get the data entry with the latest timestamp. |
*DefaultApi* | [**qualificationsGet**](Apis/DefaultApi.md#qualificationsget) | **GET** /qualifications | Retrieve all qualification data |
*DefaultApi* | [**qualificationsPost**](Apis/DefaultApi.md#qualificationspost) | **POST** /qualifications | Create a new qualification entry for a user. Fails on existing UserID |
*DefaultApi* | [**qualificationsUserIdGet**](Apis/DefaultApi.md#qualificationsuseridget) | **GET** /qualifications/{user_id} | Retrieve qualification data for a specific user |
*DefaultApi* | [**qualificationsUserIdPatch**](Apis/DefaultApi.md#qualificationsuseridpatch) | **PATCH** /qualifications/{user_id} | Update a qualification entry for a user. Unique items included in any completable item field are appended to that field. Any duplicate completable item is disregarded within that given field. |
*DefaultApi* | [**usersGet**](Apis/DefaultApi.md#usersget) | **GET** /users | Retrieve all user data |
*DefaultApi* | [**usersPost**](Apis/DefaultApi.md#userspost) | **POST** /users | Create a new user. Fails on existing UserID |
*DefaultApi* | [**usersUserIdGet**](Apis/DefaultApi.md#usersuseridget) | **GET** /users/{user_id} | Retrieve user data for a specific user |
*DefaultApi* | [**usersUserIdPatch**](Apis/DefaultApi.md#usersuseridpatch) | **PATCH** /users/{user_id} | Update data for an existing user |
*DefaultApi* | [**visitsGet**](Apis/DefaultApi.md#visitsget) | **GET** /visits | Retrieve all visit data |
*DefaultApi* | [**visitsPost**](Apis/DefaultApi.md#visitspost) | **POST** /visits | Create a new visit entry. Fails on existing UserID and Timestamp |
*DefaultApi* | [**visitsUserIdGet**](Apis/DefaultApi.md#visitsuseridget) | **GET** /visits/{user_id} | Retrieve all visits for a specific user |


<a name="documentation-for-models"></a>
## Documentation for Models

 - [3dPrinterInfo](./Models/3dPrinterInfo.md)
 - [EquipmentUsage](./Models/EquipmentUsage.md)
 - [EquipmentUsageProperties](./Models/EquipmentUsageProperties.md)
 - [EquipmentUsageRequiredProperties](./Models/EquipmentUsageRequiredProperties.md)
 - [EquipmentUsages](./Models/EquipmentUsages.md)
 - [Qualification](./Models/Qualification.md)
 - [Qualifications](./Models/Qualifications.md)
 - [QualificationsProperties](./Models/QualificationsProperties.md)
 - [User](./Models/User.md)
 - [UserID](./Models/UserID.md)
 - [UserProperties](./Models/UserProperties.md)
 - [UserRequiredProperties](./Models/UserRequiredProperties.md)
 - [Users](./Models/Users.md)
 - [Visit](./Models/Visit.md)
 - [VisitProperties](./Models/VisitProperties.md)
 - [Visits](./Models/Visits.md)
 - [400 Response](./Models/400_response.md)
 - [completableItem](./Models/completableItem.md)
 - [location](./Models/location.md)
 - [major](./Models/major.md)
 - [undergraduateClass](./Models/undergraduateClass.md)
 - [universityStatus](./Models/universityStatus.md)


<a name="documentation-for-authorization"></a>
## Documentation for Authorization

<a name="ApiKeyAuth"></a>
### ApiKeyAuth

- **Type**: API key
- **API key parameter name**: x-api-key
- **Location**: HTTP header

