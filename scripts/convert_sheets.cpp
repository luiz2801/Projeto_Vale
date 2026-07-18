#include <iostream>
#include <fstream>
#include <string>
#include <OpenXLSX.hpp>

using namespace std;
using namespace OpenXLSX;

int main(int argc, char* argv[]) {
    if (argc != 3) {
        cerr << "Erro: Número incorreto de argumentos." << endl;
        cerr << "Uso: " << argv[0] << " <arquivo_origem.xlsx> <arquivo_destino.csv>" << endl;
        return 1;
    }

    string arquivoOrigem  = argv[1];
    string arquivoDestino = argv[2];

    try {
        XLDocument doc;
        doc.open(arquivoOrigem);

        auto wks = doc.workbook().worksheet(doc.workbook().worksheetNames()[0]);

        ofstream csvFile(arquivoDestino);
        if (!csvFile.is_open()) {
            cerr << "Erro ao criar o arquivo de destino: " << arquivoDestino << endl;
            return 1;
        }

        for (uint32_t row = 1; row <= wks.rowCount(); ++row) {
            for (uint32_t col = 1; col <= wks.columnCount(); ++col) {
                
                // --- MODIFICAÇÃO SEGURA AQUI ---
                // Pegamos o objeto XLCellValue primeiro
                XLCellValue value = wks.cell(row, col).value();
                string cellValue;

                // Avalia o tipo correto para evitar o crash
                switch (value.type()) {
                    case XLValueType::Integer:
                        cellValue = to_string(value.get<int64_t>());
                        break;
                    case XLValueType::Float:
                        cellValue = to_string(value.get<double>());
                        break;
                    case XLValueType::Boolean:
                        cellValue = value.get<bool>() ? "True" : "False";
                        break;
                    case XLValueType::String:
                        cellValue = value.get<string>();
                        break;
                    case XLValueType::Empty:
                    default:
                        cellValue = "";
                        break;
                }
                // --------------------------------

                // Tratamento básico para CSV
                if (cellValue.find(',') != string::npos || cellValue.find('"') != string::npos) {
                    size_t pos = 0;
                    while ((pos = cellValue.find('"', pos)) != string::npos) {
                        cellValue.replace(pos, 1, "\"\"");
                        pos += 2;
                    }
                    csvFile << "\"" << cellValue << "\"";
                } else {
                    csvFile << cellValue;
                }

                if (col < wks.columnCount()) {
                    csvFile << ",";
                }
            }
            csvFile << "\n";
        }

        csvFile.close();
        doc.close();
        
        cout << "Conversão concluída com sucesso: " << arquivoDestino << endl;

    } catch (const exception& e) {
        cerr << "Erro durante a conversão: " << e.what() << endl;
        return 1;
    }

    return 0;
}