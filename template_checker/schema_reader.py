import yaml

class SchemaType:
    def __init__(self, schema):
        if "schema" not in schema:
            raise Exception("Schema is missing top level schema element")
        if "service_input_type" in schema["schema"]:
            self.template_type = "SERVICE"
            self.schema_path = "service_input_type"
            self.is_service = True
            self.is_env = False
            self.pipeline_present =  "pipeline_input_type" in schema["schema"]
        elif "environment_input_type" in schema["schema"]:
            self.template_type = "ENVIRONMENT"
            self.schema_path = "environment_input_type"
            self.is_service = False
            self.is_env = True
            self.pipeline_present = False
        else:
            raise Exception("Neither service nor environment input types were defined in the schema")

class SchemaReader:
    def __init__(self, templateDir):
        self.templateDir = templateDir
        self.schema = None
    
    # Opens the schema file and parses the YAML
    def __read_schema(self):
        if self.schema is not None:
             return self.schema

        # Open the schema file for this template directory, 
        # read the YAML and return the values.             
        try:
            with open(self.templateDir.schema_path(), "r") as schemaStream:
                self.schema = yaml.safe_load(schemaStream)
                if self.schema is None:
                    raise Exception("The schema file has no content")
                return self.schema
        except yaml.YAMLError as exc:
            raise Exception("Schema YAML is invalid: " + str(exc))

    def schema_type(self):
        try:
            schema = self.__read_schema()
            return SchemaType(schema)     
        except Exception as e:
            raise Exception("Error reading the schema file: " + str(e))

    # Some values in the customer authored schema have default values.
    # We'll merge these default values with the values provided by the customer
    # in the sample spec. 
    def schema_defaults(self):
        try:
            schema = self.__read_schema()
            schema_type = self.schema_type()
            schema_input_type_name = schema["schema"][schema_type.schema_path]
            schema_parameters = schema["schema"]["types"][schema_input_type_name]["properties"]
            property_defaults = {}
            for property, definition in schema_parameters.items():
                # TODO make this case insensitive
                if ("default" in definition): 
                    property_defaults[property] = definition["default"]
            return property_defaults    
        except Exception as e:
            raise Exception("Error reading from the schema file (make sure your schema is valid): " + str(e))


    def pipeline_schema_defaults(self):
        try:
            schema = self.__read_schema()
            schema_input_type_name = schema["schema"]["pipeline_input_type"]
            schema_parameters = schema["schema"]["types"][schema_input_type_name]["properties"]
            property_defaults = {}
            for property, definition in schema_parameters.items():
                # TODO make this case insensitive
                if ("default" in definition): 
                    property_defaults[property] = definition["default"]
            return property_defaults    
        except Exception as e:
            raise Exception("Error reading from the schema file (make sure your schema is valid): " + str(e))
