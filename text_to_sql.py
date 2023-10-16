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


# Define the initial system context
context = [{'role': 'system', 'content': """You are an SQL bot designed to help users create SQL commands.Your responses should begin with "This is your SQL," followed by the SQL statement that fulfills the user's request.Your database consists of SQL tables, and your goal is to generatr SQL query that can be complex with multiple joins but should optimized and specific to the requiremnets. Display the SQL command in white letters on a black background in a propar SQL format with copy feature. If the request can't be met with SQL, kindly suggest they ask for a SQL-related request."""}]

context.append( {'role':'system', 'content':"""dict with table name as key and value as list of column names
{CarrierDropReason: [Id, Reason, InsertedDate], CarrierOptions: [Id, LoadId, Price, McNumber, DotNumber, PhoneNumber, CreatedDate, CreatedAgentId, NoteText, BookedWithName, IsDeleted, CarrierId], CustomerContractLaneLoadMatch: [Id, LoadId, LaneId, ContractName, Ranking, MatchingMode, UpdatingAgentId, UpdatedDate], Industry: [Id, Name], LoadInfo: [Id, LoadId, ShipperId, SName, SAddress, SCity, SState, SZip, SContact, SEmail, SPhone, SFax, PickupNumber, PickupDate, STimeIn, STimeOut, IsShipBlind, SInstructions, SDirections, ConsigneeId, CName, CAddress, CCity, CState, CZip, CContact, CEmail, CPhone, CFax, DeliveryNumber, DeliveryDate, CTimeIn, CTimeOut, IsConsBlind, CInstructions, CDirections, BookedWith, Equipment, Driver, DriverCel, TruckNumber, TrailerNumber, RefNumber, Miles, CarrierOfficeId, SAddress2, CAddress2, cTime, sTime, ProductCategoryId, SCountry, CCountry, BookedWithTel, BookedWithEmail, CreateDate, CreateAgentId, UpdateDate, UpdateAgentId, PickupTimeStart, PickupTimeEnd, PickupTime, PickupTimeType, DeliveryTimeStart, DeliveryTimeEnd, DeliveryTime, DeliveryTimeType, PickupDateTimeUtc, DeliveryDateTimeUtc, ProductValueId, DriverHour], agents: [Id, Login, Password, Name, Address, City, State, Zip, Country, Tel, Cel, Fax, Email, OfficeId, RoleId, IsShare, CommonRate, IsNightAccess, CarrierInstructions, UpdateDate, UpdateAgentId, Address2, QuickBooksId, HireDate, ReleaseDate, SpecialCategoryId, HasDATAccess, DATLogin, DATPassword, CompensationTeamId, CustomQuotaSourceId, CustomMarginSourceId, DivisionId, CustomQuota, DepartmentId, AgentGuid, IsModified, TitleId, Ext, IsCustomQuotaSource, IsCustomMarginSource, IsTitleFutureDated, NonEmployee, AdAuthentication], carriercontact: [Id, CarrierId, Name, Title, Phone, PhoneExt, Fax, Cell, Email, Notes, IsDeleted, CreatedDate, UpdatedDate, CreatedAgentId, UpdatedAgentId], carriers: [Id, MCNumber, Status, Equipment, Name, Address, Address2, City, State, Zip, Country, Phone, Cel, Fax, TollFree, Email, Website, Note, EquipmentNote, DispatchNote, UpdateDate, UpdateAgentId], crm_carrierprofile: [Id, CarrierId, CRMCarrierStatusId, UpdatingDate, UpdatingAgentId, PrimaryContactId, IsStale], crm_carrierreps: [Id, CarrierId, RepAgentId, CreatedDate, CreatedAgentId, RemovedDate, RemovedAgentId, RepType], crm_carrierstatuses: [Id, Name], customers: [Id, Name, Phone, Fax, Cell, TollFree, Email, WebSite, UpdateDateTime, UpdateAgentId, MasterCustomerId, CallTime, AgentId, Notes, DispatchNotes, AccountsPayable, AccountsEmail, Shared, CreateDateTime, NotableId, SalespersonId, EstimatedVolume, PersonalInfo, CurrentBrokerPartner, CurrentFreightChallenges, IsProduce, CustomerLeadSourceId, IndustryId, Is214Edi, ExclDrayMarginBeforePickup, NoPost, IsCustomer, Commodity, EstimatedVolumeTimePeriodId, TenderMethodId, SicCode, NaicsCode, NextRfpDate, AwardPeriodId, NationalSalesRepId, SalesManagerRepId, CreatedAgentId, IsStale, CalculatedStatus, IsAtRisk, SoftDeleted, AcquisitionSourceId, AcquisitionDate, DeadDate, RawPhone, RawCell, AccessorialEmailAddress], datmarket: [Id, ReferenceCity, ReferenceState, MarketAreaId, MarketAreaName, MarketMapUrl], equipmentgroups: [Equipment, Equipment_Group, EquipmentId], fm_CarrierRemovedAndAdded: [LoadId, CarrierRemovedDate, RemovingAgentId, RemovedCarrierId, ChangeReasonId, OldCarrierRate, LastDispatcherId, NextCarrierAddedTime, LastCarrierAddedTime, RemovedReason, AddingAgentId, NewCarrierId, NewCarrierRate, CarrierOriginallyAddedAgentId], geoloc: [GeoLocId, City, State, Lat, Lon, CLat, SLat, Zip, Country], industry: [Id, Name], linehaulrates: [LoadId, CarrierLinehaul, CustomerLinehaul], loadinfo: [Id, LoadId, ShipperId, SName, SAddress, SCity, SState, SZip, SContact, SEmail, SPhone, SFax, PickupNumber, PickupDate, STimeIn, STimeOut, IsShipBlind, SInstructions, SDirections, ConsigneeId, CName, CAddress, CCity, CState, CZip, CContact, CEmail, CPhone, CFax, DeliveryNumber, DeliveryDate, CTimeIn, CTimeOut, IsConsBlind, CInstructions, CDirections, BookedWith, Equipment, Driver, DriverCel, TruckNumber, TrailerNumber, RefNumber, Miles, CarrierOfficeId, SAddress2, CAddress2, cTime, sTime, ProductCategoryId, SCountry, CCountry, BookedWithTel, BookedWithEmail, CreateDate, CreateAgentId, UpdateDate, UpdateAgentId, PickupTimeStart, PickupTimeEnd, PickupTime, PickupTimeType, DeliveryTimeStart, DeliveryTimeEnd, DeliveryTime, DeliveryTimeType, PickupDateTimeUtc, DeliveryDateTimeUtc, ProductValueId, DriverHour], loads: [Id, Status, SalespersonId, DispatcherId, CreateDate, CustomerRate, CarrierRate, Notes, IsPostLoadBoard, DispatchNotes, CustomerId, FirstLoadInfoId, CustomerPO, CustomerBL, SuperStatus, PrintedDate, PostedDate, CarrierId, TotalCustomerRate, TotalCarrierRate, InvoiceId, BillId, Aging, Currenttimestamp, OfficeId, AuditStatus, TotalCarrierAdj, GrossProfitAmt, AccountManagerId, BkgNbr, CntNbr, StatusId, Update214Edi, StatusReasonId, NetSuiteLoadId, CreateAgentId, UpdateDate, UpdateAgentId, PayUpTo, NotableId, NoTrack, TrackerId, CsRepId, NoPost, ExcludeRate, ProductionLoad, AgingStartDate], loadstatushistory: [LoadStatusHistoryId, AgentId, LoadId, LoadStatusId, UpdateTime, StatusReasonId, StopNo], mastercustomers: [Id, Name, BillingAddr, City, State, Phone, Fax, Status, PoDRequired, QuickBookBalance, CreditLimit, TermsOfPay, CreditAppReceived, InvoiceMethod, CreditRating, UpdateDateTime, SyncDateTime, UpdateAgentId, Zip, Country, FATSBalance, FinanceNotes, Notes, IsCustomer, QuickBooksId, BillingAddr2, CustomerDate, chDelayDate, Location, Dba, WebSite, CompanyNameOnInvoice, DbaNameOnInvoice, PhysicalAddress1, PhysicalAddress2, PhysicalCity, PhysicalCountry, PhysicalState, PhysicalZip, MethodOfPayment], offices: [Id, Name, Address, Address2, City, State, Zip, Country, Phone, Fax, Wats, Email, UpdateDateTime, UpdateAgentId, IsActive, IsSupport, DefaultDATLogin, DepartmentId, TimeZoneId, IsCityState, OfficeDepartmentId, RegionId, TrackerEmail, DATPassword, DATUserName], tenderingtms: [Id, Name], trip: [LoadId, StatusId, CarrierId, EquipmentId, Equipment, StopCount, FirstLoadInfoId, PickupDateTimeServer, PickupDateTimeUtc, PickupGeoLocId, PickupCity, PickupState, PickupZip, LastLoadInfoId, DeliveryDateTimeServer, DeliveryDateTimeUtc, DeliveryGeoLocId, DeliveryCity, DeliveryState, DeliveryZip, CargoWeight, IsTonu, IsStorage, IsAddendum, Miles, MasterCustomerId, MasterCustomerName, CarrierName, EquipmentGroupId, ProductCategoryId, SalespersonId, SalespersonName, DispatcherId, DispatcherName, TrackerId, TrackerName, ShipperNames, ConsigneeNames, PickupNumbers, DeliveryNumbers, CarrierRefNumbers, PickupTimeStart, PickupTimeEnd, DeliveryTimeStart, DeliveryTimeEnd, FirstShipperName, LastConsigneeName, PickupTime, DeliveryTime, Commodity, PickupLocationId, DeliveryLocationId, IsShellLoad, LoadStatusRank, ExclFromReports, PickupMarketId, DeliveryMarketId, CargoType, CargoClass, CsRepId, CsRepName, IsDropTrailer, CargoQuantity, OverDim]}"""
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



