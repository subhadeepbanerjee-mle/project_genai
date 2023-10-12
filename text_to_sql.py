import openai
import streamlit as st

# set api key
openai.api_key = st.secrets["pass"]

st.header ("Text to SQL generator using OpenAi")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != 'system':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])



# def continue_conversation(messages, temperature=0):
#     """
#     Continue a conversation using the OpenAI GPT-3 model.

#     Args:
#         messages (list): List of message objects containing role and content.
#         temperature (float): Sampling temperature for response generation.

#     Returns:
#         str: The response message content.
#     """
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=messages,
#         temperature=temperature,
#     )
#     return response.choices[0].message["content"]


context = [{'role': 'system', 'content': """
            You are an SQL bot designed to help users create SQL commands.\
            Your responses should begin with "This is your SQL," \
            followed by the SQL statement that fulfills the user's request. \
            Your database consists of SQL tables, and your goal is to keep SQL \
            commands straightforward. Display the SQL command in white letters\
            on a black background, followed by a brief and clear explanation of \
            how it functions. If a user requests something that cannot be \
            achieved with an SQL command, provide a polite and simple response,\
            and encourage them to ask for a SQL-related request."""}]

# context.append( {'role':'system', 'content':"""
# first table:
# {'table name': 'eiaweeklydieselprice',
# 'columns': ['recordSurrogateKey', 'Week', 'PricePerGallon', 'WeeklyChange', 'YearlyChange', 'recordCreatedTimestamp'],
# 'data types': [StringType, DateType, DecimalType(18,3), DecimalType(18,3), DecimalType(18,3), TimestampType]}
# """
# })

context.append( {'role':'system', 'content':"""
{'table name': 'CarrierDropReason', 'columns': ['Id', 'Reason', 'InsertedDate', 'recordCreatedTimestamp']}
{'table name': 'CarrierOptions', 'columns': ['Id', 'LoadId', 'Price', 'McNumber', 'DotNumber', 'PhoneNumber', 'CreatedDate', 'CreatedAgentId', 'NoteText', 'BookedWithName', 'IsDeleted', 'CarrierId', 'recordCreatedTimestamp']}
{'table name': 'CustomerContractLaneLoadMatch', 'columns': ['Id', 'LoadId', 'LaneId', 'ContractName', 'Ranking', 'MatchingMode', 'UpdatingAgentId', 'UpdatedDate', 'recordCreatedTimestamp']}
{'table name': 'Industry', 'columns': ['Id', 'Name', 'recordCreatedTimestamp']}
{'table name': 'LoadInfo', 'columns': ['Id', 'LoadId', 'ShipperId', 'SName', 'SAddress', 'SCity', 'SState', 'SZip', 'SContact', 'SEmail', 'SPhone', 'SFax', 'PickupNumber', 'PickupDate', 'STimeIn', 'STimeOut', 'IsShipBlind', 'SInstructions', 'SDirections', 'ConsigneeId', 'CName', 'CAddress', 'CCity', 'CState', 'CZip', 'CContact', 'CEmail', 'CPhone', 'CFax', 'DeliveryNumber', 'DeliveryDate', 'CTimeIn', 'CTimeOut', 'IsConsBlind', 'CInstructions', 'CDirections', 'BookedWith', 'Equipment', 'Driver', 'DriverCel', 'TruckNumber', 'TrailerNumber', 'RefNumber', 'Miles', 'CarrierOfficeId', 'SAddress2', 'CAddress2', 'cTime', 'sTime', 'ProductCategoryId', 'SCountry', 'CCountry', 'BookedWithTel', 'BookedWithEmail', 'CreateDate', 'CreateAgentId', 'UpdateDate', 'UpdateAgentId', 'PickupTimeStart', 'PickupTimeEnd', 'PickupTime', 'PickupTimeType', 'DeliveryTimeStart', 'DeliveryTimeEnd', 'DeliveryTime', 'DeliveryTimeType', 'PickupDateTimeUtc', 'DeliveryDateTimeUtc', 'ProductValueId', 'DriverHour', 'Temperature', 'Driver2', 'Driver2Cel', 'IsShipDropTrailer', 'IsConsDropTrailer', 'ShipDriverInDate', 'ShipDriverOutDate', 'ConsDriverInDate', 'ConsDriverOutDate', 'TemperatureText', 'PickupStartDate', 'PickupEndDate', 'DeliveryStartDate', 'DeliveryEndDate', 'TruckYear', 'TrailerYear', 'ReeferUnitYear', 'TrailerChute', 'AirCargoShipment', 'TSAChange6ATestDate', 'TSAChange6ATestScore', 'TSAIdMethod', 'TSAIdNumber', 'CLatitude', 'CLongitude', 'SLatitude', 'SLongitude', 'Height', 'Length', 'OverDim', 'Weight', 'Width', 'EquipmentLength', 'recordCreatedTimestamp']}
{'table name': 'agents', 'columns': ['Id', 'Login', 'Password', 'Name', 'Address', 'City', 'State', 'Zip', 'Country', 'Tel', 'Cel', 'Fax', 'Email', 'OfficeId', 'RoleId', 'IsShare', 'CommonRate', 'IsNightAccess', 'CarrierInstructions', 'UpdateDate', 'UpdateAgentId', 'Address2', 'QuickBooksId', 'HireDate', 'ReleaseDate', 'SpecialCategoryId', 'HasDATAccess', 'DATLogin', 'DATPassword', 'CompensationTeamId', 'CustomQuotaSourceId', 'CustomMarginSourceId', 'DivisionId', 'CustomQuota', 'DepartmentId', 'AgentGuid', 'IsModified', 'TitleId', 'Ext', 'IsCustomQuotaSource', 'IsCustomMarginSource', 'IsTitleFutureDated', 'NonEmployee', 'AdAuthentication', 'recordCreatedTimestamp']}
{'table name': 'carriercontact', 'columns': ['Id', 'CarrierId', 'Name', 'Title', 'Phone', 'PhoneExt', 'Fax', 'Cell', 'Email', 'Notes', 'IsDeleted', 'CreatedDate', 'UpdatedDate', 'CreatedAgentId', 'UpdatedAgentId', 'recordCreatedTimestamp']}
{'table name': 'carriers', 'columns': ['Id', 'MCNumber', 'Status', 'Equipment', 'Name', 'Address', 'Address2', 'City', 'State', 'Zip', 'Country', 'Phone', 'Cel', 'Fax', 'TollFree', 'Email', 'Website', 'Note', 'EquipmentNote', 'DispatchNote', 'UpdateDate', 'UpdateAgentId', 'SyncDate', 'ActivateDate', 'ActivateAgentId', 'PowerUnits', 'Mileage', 'W9', 'QuickPay', 'QuickBooksId', 'FactorName', 'FactorEmail', 'UseAltAddress', 'NOAOnFile', 'ClaimPending', 'AssignedAgentId', 'FactorId', 'DbaName', 'IsQBNameChange', 'OverrideName', 'DOTNumber', 'PODEmail', 'NOAEffectiveDate', 'QuickBooksVendorName', 'GoldStar', 'AllowBrokerAuthority', 'HubTranId', 'DisableSaferEmail', 'RequireCSBooking', 'RestrictRVBooking', 'SaferWatchContact1', 'SaferWatchContact2', 'SaferWatchContactPhone', 'SaferWatchContactEmail', 'CarrierType', 'Trucks', 'Trailers', 'TotalDriverCount', 'LeasedDriverCount', 'NoteSoftDeleted', 'Mcs150Date', 'StatusId', 'AcquisitionSourceId', 'AcquisitionDate', 'RhinoLinkApproved', 'recordCreatedTimestamp']}
{'table name': 'crm_carrierprofile', 'columns': ['Id', 'CarrierId', 'CRMCarrierStatusId', 'UpdatingDate', 'UpdatingAgentId', 'PrimaryContactId', 'IsStale', 'recordCreatedTimestamp']}
{'table name': 'crm_carrierreps', 'columns': ['Id', 'CarrierId', 'RepAgentId', 'CreatedDate', 'CreatedAgentId', 'RemovedDate', 'RemovedAgentId', 'RepType', 'recordCreatedTimestamp']}
{'table name': 'crm_carrierstatuses', 'columns': ['Id', 'Name', 'recordCreatedTimestamp']}
{'table name': 'customers', 'columns': ['Id', 'Name', 'Phone', 'Fax', 'Cell', 'TollFree', 'Email', 'WebSite', 'UpdateDateTime', 'UpdateAgentId', 'MasterCustomerId', 'CallTime', 'AgentId', 'Notes', 'DispatchNotes', 'AccountsPayable', 'AccountsEmail', 'Shared', 'CreateDateTime', 'NotableId', 'SalespersonId', 'EstimatedVolume', 'PersonalInfo', 'CurrentBrokerPartner', 'CurrentFreightChallenges', 'IsProduce', 'CustomerLeadSourceId', 'IndustryId', 'Is214Edi', 'ExclDrayMarginBeforePickup', 'NoPost', 'IsCustomer', 'Commodity', 'EstimatedVolumeTimePeriodId', 'TenderMethodId', 'SicCode', 'NaicsCode', 'NextRfpDate', 'AwardPeriodId', 'NationalSalesRepId', 'SalesManagerRepId', 'CreatedAgentId', 'IsStale', 'CalculatedStatus', 'IsAtRisk', 'SoftDeleted', 'AcquisitionSourceId', 'AcquisitionDate', 'DeadDate', 'RawPhone', 'RawCell', 'AccessorialEmailAddress', 'recordCreatedTimestamp']}
{'table name': 'datmarket', 'columns': ['Id', 'ReferenceCity', 'ReferenceState', 'MarketAreaId', 'MarketAreaName', 'MarketMapUrl', 'recordCreatedTimestamp']}
{'table name': 'equipmentgroups', 'columns': ['Equipment', 'Equipment_Group', 'EquipmentId', 'recordCreatedTimestamp']}
{'table name': 'fm_CarrierRemovedAndAdded', 'columns': ['LoadId', 'CarrierRemovedDate', 'RemovingAgentId', 'RemovedCarrierId', 'ChangeReasonId', 'OldCarrierRate', 'LastDispatcherId', 'NextCarrierAddedTime', 'LastCarrierAddedTime', 'RemovedReason', 'AddingAgentId', 'NewCarrierId', 'NewCarrierRate', 'CarrierOriginallyAddedAgentId', 'recordCreatedTimestamp']}
{'table name': 'geoloc', 'columns': ['GeoLocId', 'City', 'State', 'Lat', 'Lon', 'CLat', 'SLat', 'Zip', 'Country', 'recordCreatedTimestamp']}
{'table name': 'industry', 'columns': ['Id', 'Name', 'recordCreatedTimestamp']}
{'table name': 'linehaulrates', 'columns': ['LoadId', 'CarrierLinehaul', 'CustomerLinehaul', 'recordCreatedTimestamp']}
{'table name': 'loadinfo', 'columns': ['Id', 'LoadId', 'ShipperId', 'SName', 'SAddress', 'SCity', 'SState', 'SZip', 'SContact', 'SEmail', 'SPhone', 'SFax', 'PickupNumber', 'PickupDate', 'STimeIn', 'STimeOut', 'IsShipBlind', 'SInstructions', 'SDirections', 'ConsigneeId', 'CName', 'CAddress', 'CCity', 'CState', 'CZip', 'CContact', 'CEmail', 'CPhone', 'CFax', 'DeliveryNumber', 'DeliveryDate', 'CTimeIn', 'CTimeOut', 'IsConsBlind', 'CInstructions', 'CDirections', 'BookedWith', 'Equipment', 'Driver', 'DriverCel', 'TruckNumber', 'TrailerNumber', 'RefNumber', 'Miles', 'CarrierOfficeId', 'SAddress2', 'CAddress2', 'cTime', 'sTime', 'ProductCategoryId', 'SCountry', 'CCountry', 'BookedWithTel', 'BookedWithEmail', 'CreateDate', 'CreateAgentId', 'UpdateDate', 'UpdateAgentId', 'PickupTimeStart', 'PickupTimeEnd', 'PickupTime', 'PickupTimeType', 'DeliveryTimeStart', 'DeliveryTimeEnd', 'DeliveryTime', 'DeliveryTimeType', 'PickupDateTimeUtc', 'DeliveryDateTimeUtc', 'ProductValueId', 'DriverHour', 'Temperature', 'Driver2', 'Driver2Cel', 'IsShipDropTrailer', 'IsConsDropTrailer', 'ShipDriverInDate', 'ShipDriverOutDate', 'ConsDriverInDate', 'ConsDriverOutDate', 'TemperatureText', 'PickupStartDate', 'PickupEndDate', 'DeliveryStartDate', 'DeliveryEndDate', 'TruckYear', 'TrailerYear', 'ReeferUnitYear', 'TrailerChute', 'AirCargoShipment', 'TSAChange6ATestDate', 'TSAChange6ATestScore', 'TSAIdMethod', 'TSAIdNumber', 'CLatitude', 'CLongitude', 'SLatitude', 'SLongitude', 'Height', 'Length', 'OverDim', 'Weight', 'Width', 'EquipmentLength', 'recordCreatedTimestamp']}
{'table name': 'loads', 'columns': ['Id', 'Status', 'SalespersonId', 'DispatcherId', 'CreateDate', 'CustomerRate', 'CarrierRate', 'Notes', 'IsPostLoadBoard', 'DispatchNotes', 'CustomerId', 'FirstLoadInfoId', 'CustomerPO', 'CustomerBL', 'SuperStatus', 'PrintedDate', 'PostedDate', 'CarrierId', 'TotalCustomerRate', 'TotalCarrierRate', 'InvoiceId', 'BillId', 'Aging', 'Currenttimestamp', 'OfficeId', 'AuditStatus', 'TotalCarrierAdj', 'GrossProfitAmt', 'AccountManagerId', 'BkgNbr', 'CntNbr', 'StatusId', 'Update214Edi', 'StatusReasonId', 'NetSuiteLoadId', 'CreateAgentId', 'UpdateDate', 'UpdateAgentId', 'PayUpTo', 'NotableId', 'NoTrack', 'TrackerId', 'CsRepId', 'NoPost', 'ExcludeRate', 'ProductionLoad', 'AgingStartDate', 'recordCreatedTimestamp']}
{'table name': 'loadstatushistory', 'columns': ['LoadStatusHistoryId', 'AgentId', 'LoadId', 'LoadStatusId', 'UpdateTime', 'StatusReasonId', 'StopNo', 'StatusChangeDate', 'StatusChangeTimezone', 'TotalCustomerRate', 'TotalCarrierRateAdj', 'Edi214Sent', 'recordCreatedTimestamp']}
{'table name': 'mastercustomers', 'columns': ['Id', 'Name', 'BillingAddr', 'City', 'State', 'Phone', 'Fax', 'Status', 'PoDRequired', 'QuickBookBalance', 'CreditLimit', 'TermsOfPay', 'CreditAppReceived', 'InvoiceMethod', 'CreditRating', 'UpdateDateTime', 'SyncDateTime', 'UpdateAgentId', 'Zip', 'Country', 'FATSBalance', 'FinanceNotes', 'Notes', 'IsCustomer', 'QuickBooksId', 'BillingAddr2', 'CustomerDate', 'chDelayDate', 'Location', 'Dba', 'WebSite', 'CompanyNameOnInvoice', 'DbaNameOnInvoice', 'PhysicalAddress1', 'PhysicalAddress2', 'PhysicalCity', 'PhysicalCountry', 'PhysicalState', 'PhysicalZip', 'MethodOfPayment', 'Ext', 'UseSecondaryInvoiceMethod', 'SecondaryInvoiceMethod', 'NotableId', 'ActivateDate', 'BatchCycleTerms', 'UseCarrierNamesInPDF', 'BatchInvoiceTerms', 'IsModified', 'ARAutoEmailType', 'ParentCustomerId', 'PastDueBalance', 'PortalUrl', 'PortalUsername', 'PortalPassword', 'EulerId', 'EulerBuyerId', 'EulerCoverageAmount', 'EulerSetByParent', 'IsEulerInsured', 'InsuranceAmountRequired', 'RawName', 'RawPhone', 'RawDba', 'ForcedAudit', 'AcquisitionSourceId', 'AcquisitionDate', 'IsHighCreditRisk', 'HighCreditRiskSetByParent', 'AcquisitionTermDate', 'ClassificationId', 'recordCreatedTimestamp']}
{'table name': 'offices', 'columns': ['Id', 'Name', 'Address', 'Address2', 'City', 'State', 'Zip', 'Country', 'Phone', 'Fax', 'Wats', 'Email', 'UpdateDateTime', 'UpdateAgentId', 'IsActive', 'IsSupport', 'DefaultDATLogin', 'DepartmentId', 'TimeZoneId', 'IsCityState', 'OfficeDepartmentId', 'RegionId', 'TrackerEmail', 'DATPassword', 'DATUserName', 'recordCreatedTimestamp']}
{'table name': 'tenderingtms', 'columns': ['Id', 'Name', 'recordCreatedTimestamp']}
{'table name': 'trip', 'columns': ['LoadId', 'StatusId', 'CarrierId', 'EquipmentId', 'Equipment', 'StopCount', 'FirstLoadInfoId', 'PickupDateTimeServer', 'PickupDateTimeUtc', 'PickupGeoLocId', 'PickupCity', 'PickupState', 'PickupZip', 'LastLoadInfoId', 'DeliveryDateTimeServer', 'DeliveryDateTimeUtc', 'DeliveryGeoLocId', 'DeliveryCity', 'DeliveryState', 'DeliveryZip', 'CargoWeight', 'IsTonu', 'IsStorage', 'IsAddendum', 'Miles', 'MasterCustomerId', 'MasterCustomerName', 'CarrierName', 'EquipmentGroupId', 'ProductCategoryId', 'SalespersonId', 'SalespersonName', 'DispatcherId', 'DispatcherName', 'TrackerId', 'TrackerName', 'ShipperNames', 'ConsigneeNames', 'PickupNumbers', 'DeliveryNumbers', 'CarrierRefNumbers', 'PickupTimeStart', 'PickupTimeEnd', 'DeliveryTimeStart', 'DeliveryTimeEnd', 'FirstShipperName', 'LastConsigneeName', 'PickupTime', 'DeliveryTime', 'Commodity', 'PickupLocationId', 'DeliveryLocationId', 'IsShellLoad', 'LoadStatusRank', 'ExclFromReports', 'PickupMarketId', 'DeliveryMarketId', 'CargoType', 'CargoClass', 'CsRepId', 'CsRepName', 'IsDropTrailer', 'CargoQuantity', 'OverDim', 'recordCreatedTimestamp']}
{'table name': 'vwLastBookedTime', 'columns': ['LoadId', 'LastBookedTime', 'recordCreatedTimestamp']}
"""
})

st.session_state.messages = context


# Accept user input
if prompt := st.chat_input("Please enter your description here to generate SQL query."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})



