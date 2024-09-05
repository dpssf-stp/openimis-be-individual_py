
from dateutil import parser
from dateutil.parser import parserinfo

# field names and individual import related constants
_group_label_field = 'agregado_id'
_group_head_field = 'chefe_familia'
_group_locality_field = 'localidade'
_group_default_program_status_field = 'estado_pfv'
_group_default_program_problem_field = 'problema_id'
_group_vulnerability_category_field = 'categoria_vulnerabilidade'
_group_contact_number_field = 'contacto_telefonico'

_full_name_field = 'nome'
_nickname_field = 'vulgo'
_dob_field = 'data_de_nascimento'
_id_number_field = 'num_doc_id'
_id_unique_field = 'id_ind'
_sex_field = 'sexo'
_district_field = 'distrito'
_sub_district_field = 'subdistrito'
_pmt_field = 'PMT'
_id_front_url_field = 'download_url_foto_doc_id'
_id_back_url_field = 'download_url_doc_id_verso'

_date_format = "%d/%m/%Y"
_secondary_date_format = "%Y-%m-%d"


# other constants
no_change_error_message = 'there are no changes'


# Define a custom parser with specific date formats
class IndividualImportDateParserInfo(parserinfo):
    # Define the date formats to be considered
    DATEFORMATS = [
        _date_format,  # DD/MM/YYYY
        _secondary_date_format,  # YYYY/MM/DD
    ]

# Create a parser instance using the custom parser info
individual_date_parser = parser.parser(IndividualImportDateParserInfo())