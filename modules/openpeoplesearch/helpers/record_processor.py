from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform, UIM_DEBUG
from maltego_trx.entities import Location, Person, Email, PhoneNumber, Company, Phrase

class RecordProcessor:
    @staticmethod
    def process_record(record, response):
        
        field_names = [
            "reportedDate", "firstName", "middleName", "lastName", "address", 
            "city", "state", "zip", "email", "phone", "lineType", "dob", 
            "occupation", "employer", "associatedDomain", "dataTypeName", 
            "dataCategoryName", "webVerificationLink", "vol", "recordId"
        ]

        # Ensure each field is capitalized, if it's a string
        fields = {field: record.get(field, "").title() if isinstance(record.get(field, ""), str) else record.get(field, "") for field in field_names}

        # Full name calculation now includes capitalized names
        fullname = fields['firstName'] + " " + fields['lastName']

        entity = response.addEntity(Person, fullname)

        # Adding properties to the entity object with capitalized values
        entity.addProperty(fieldName="person.fullname", displayName="Full Name", value=fullname)
        entity.addProperty(fieldName="person.firstnames", displayName="First Names", value=fields['firstName'])
        entity.addProperty(fieldName="middlename", displayName="Middle Name", value=fields['middleName'])
        entity.addProperty(fieldName="person.lastname", displayName="Last Name", value=fields['lastName'])
        entity.addProperty(fieldName="dob", displayName="Date of Birth", value=fields['dob'])
        entity.addProperty(fieldName='email', displayName='Email Address', value=fields['email'])
        entity.addProperty(fieldName='phonenumber', displayName='Phone Number', value=fields['phone'])
        entity.addProperty(fieldName='linetype', displayName='Line Type', value=fields['lineType'])
        entity.addProperty(fieldName="streetaddress", displayName="Street Address", value=fields['address'])
        entity.addProperty(fieldName="city", displayName="City", value=fields['city'])
        entity.addProperty(fieldName="state", displayName="State", value=fields['state'])
        entity.addProperty(fieldName="zipcode", displayName="Zip Code", value=fields['zip'])
        entity.addProperty(fieldName="occupation", displayName="Occupation", value=fields['occupation'])
        entity.addProperty(fieldName="employer", displayName="Employer", value=fields['employer'])
        entity.addProperty(fieldName="record_id", displayName="OPS Record ID", value=fields['recordId'], matchingRule='strict')
        entity.addProperty(fieldName="reportedDate", displayName="Reported Date", value=fields['reportedDate'])
        entity.addProperty(fieldName='associated_domain', displayName='Associated Domain', value=fields['associatedDomain'])
        entity.addProperty(fieldName='data_type_name', displayName='Data Type', value=fields['dataTypeName'])
        entity.addProperty(fieldName='data_category_name', displayName='Data Category', value=fields['dataCategoryName'])
        entity.addProperty(fieldName='web_verification_link', displayName='Verification Link', value=fields['webVerificationLink'])
        entity.addProperty(fieldName='vol', displayName='Vol', value=fields['vol'])

        return entity
