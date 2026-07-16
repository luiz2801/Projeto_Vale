#include <iostream>
#include <memory>
#include <arrow/api.h>
#include <arrow/io/api.h>
#include <arrow/csv/api.h>
#include <parquet/arrow/reader.h>

int main(int argc, char** argv) {
    // Verifica se o usuário passou os 2 argumentos necessários
    if (argc < 3) {
        std::cerr << "Uso: " << argv[0] << " <arquivo_entrada.parquet> <arquivo_saida.csv>" << std::endl;
        return 1;
    }

    std::string input_file = argv[1];
    std::string output_file = argv[2];

    arrow::MemoryPool* pool = arrow::default_memory_pool();
    
    // 1. Abrir o arquivo Parquet de entrada
    auto input_result = arrow::io::ReadableFile::Open(input_file);
    if (!input_result.ok()) {
        std::cerr << "Erro ao abrir '" << input_file << "': " << input_result.status().ToString() << std::endl;
        return 1;
    }
    std::shared_ptr<arrow::io::ReadableFile> input = std::move(input_result).ValueOrDie();

    // 2. Abrir o leitor do Parquet
    auto reader_result = parquet::arrow::OpenFile(input, pool);
    if (!reader_result.ok()) {
        std::cerr << "Erro no leitor Parquet: " << reader_result.status().ToString() << std::endl;
        return 1;
    }
    std::unique_ptr<parquet::arrow::FileReader> arrow_reader = std::move(reader_result).ValueOrDie();

    // 3. Ler para Table
    std::shared_ptr<arrow::Table> table;
    auto read_status = arrow_reader->ReadTable(&table);
    if (!read_status.ok()) {
        std::cerr << "Erro ao ler tabela: " << read_status.ToString() << std::endl;
        return 1;
    }

    // 4. Salvar como CSV
    auto output_result = arrow::io::FileOutputStream::Open(output_file);
    if (!output_result.ok()) {
        std::cerr << "Erro ao criar '" << output_file << "': " << output_result.status().ToString() << std::endl;
        return 1;
    }
    std::shared_ptr<arrow::io::FileOutputStream> output = std::move(output_result).ValueOrDie();

    auto write_options = arrow::csv::WriteOptions::Defaults();
    auto write_status = arrow::csv::WriteCSV(*table, write_options, output.get());

    if (write_status.ok()) {
        std::cout << "Convertido: " << input_file << " -> " << output_file << std::endl;
    } else {
        std::cerr << "Erro na escrita: " << write_status.ToString() << std::endl;
        return 1;
    }

    return 0;
}
