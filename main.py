from gateway.vw_gateway import VisWaxGateway
from services.parser_service import ParserService
import json

if __name__ == "__main__":

    vw_gateway = VisWaxGateway()
    parser_service = ParserService()

    fc_data = vw_gateway.fetch_from_fc()
    tiamat_data = vw_gateway.fetch_from_alt()
    output = parser_service.retrieve_viswax_details_from_source(fc_data, tiamat_data)

    with open('./viswax.json', 'w') as f:
        json.dump(output, f, indent=4)

    print(output)
