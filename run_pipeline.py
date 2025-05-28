#!/usr/bin/env python3
"""
Script to run the full data processing pipeline.
"""
from src.data_processing import process_all

if __name__ == '__main__':
    input_csv = 'IC_Dados_Curados - Worksheet (1).csv'
    output_csv = 'IC_Dados_Processados.csv'
    codebook_txt = 'Livro_de_Codigos.txt'
    print(f"Running pipeline: {input_csv} -> {output_csv}, {codebook_txt}")
    df = process_all(input_csv, output_csv, codebook_txt)
    print("Pipeline executed successfully.") 