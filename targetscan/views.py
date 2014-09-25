__author__ = 'pcmarks'

import leveldb
import csv
from json import JSONDecoder
import os
import collections
import re

from django.http import HttpResponse
from django.shortcuts import render

from forms import TargetScanForm


outer_directory = "/home/pcmarks/Work/MMCRI/duarte/miRNA TargetScan/data/database"
database_directory = os.path.join(outer_directory, 'targetscan_db')


def targetScan(request):
    """

    :param request:
    :return:
    """
    miRNA_list = []
    all_gene_list = []
    context_score_threshold = 0.0
    miRNA_gene_matches = 0
    download_results = False
    if request.method == 'POST':
        if 'download' in request.POST:
            download_results = True
        form = TargetScanForm(request.POST, request.FILES)
        if form.is_valid():
            max_no_genes = form.cleaned_data['maximum_no_of_genes']
            max_no_genes = int(max_no_genes)
            max_no_occurrences = form.cleaned_data['maximum_no_of_occurrences']
            max_no_occurrences = int(max_no_occurrences)
            if download_results:
                max_no_genes = 0        # This gets all of the genes
            x = form.cleaned_data['miRNA'].strip()
            if len(x) == 0:
                miRNA_symbols = None
            else:
                y = re.sub(r'\s+', ' ', x).strip()
                miRNA_symbols = y.split(' ')
            context_score_threshold = form.cleaned_data['context_score_threshold']
            context_score_threshold = float(context_score_threshold)
            if miRNA_symbols:
                total_no_gene_hits = 0

                for miRNA_symbol in miRNA_symbols:
                    if miRNA_symbol:
                        result = {'miRNA_symbol': miRNA_symbol}
                        (no_of_hits, gene_score_list, gene_list) = \
                            retrieve_gene_list(miRNA_symbol, max_no_genes, context_score_threshold)
                        if gene_score_list:
                            result['gene_list'] = gene_score_list
                            result['no_of_hits'] = no_of_hits
                            total_no_gene_hits += 1
                            all_gene_list.extend(gene_list)
                        miRNA_list.append(result)
                miRNA_gene_matches = total_no_gene_hits
        if len(all_gene_list) == 0:
            return render(request,
                          'targetScan.html',
                          {'form': form, 'result_message': "No matches found for the miRNA symbol(s).",
                           'results': None})
        counter = collections.Counter(all_gene_list)
        occurrences = counter.most_common(max_no_occurrences)
        gene_symbols = ' '.join(map(lambda x: x[0], occurrences))
        if download_results:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=results.csv'
            writer = csv.writer(response)
            for result in miRNA_list:
                if 'gene_list' in result:
                    miRNA_symbol = result['miRNA_symbol']
                    genes = result['gene_list']
                    for gene, score in genes:
                        writer.writerow([miRNA_symbol, gene, score])
            return response
        else:
            return render(request,
                          'targetScan.html',
                          {'form': form, 'occurrences': occurrences, 'results': miRNA_list,
                           'context_score_threshold': context_score_threshold,
                           'miRNA_gene_matches': miRNA_gene_matches,
                           'gene_symbols': gene_symbols})
    else:
        form = TargetScanForm()
        return render(request, 'targetScan.html', {'form': form})


def download(request, miRNA_symbol):
    """

    :param request:
    :param miRNA_symbol:
    :return:
    """
    if 'cst' in request.GET:
        cst = request.GET['cst']
    else:
        cst = '0.0'
    context_score_threshold = float(cst)
    (no_of_hits, gene_score_list, gene_list) = retrieve_gene_list(miRNA_symbol, 0, context_score_threshold)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % miRNA_symbol
    writer = csv.writer(response)
    for gene_entry in gene_score_list:
        writer.writerow([gene_entry[0], gene_entry[1]])
    return response


def retrieve_gene_list(symbol, max_no_genes, context_score_threshold):
    """

    :param symbol:
    :param max_no_genes:
    :param context_score_threshold:
    :return:
    """
    gene_list = None
    gene_score_list = None
    no_of_hits = 0
    if symbol:
        db = leveldb.LevelDB(database_directory)
        key = 'targetScan/02/%s/03' % symbol
        try:
            json_data = db.Get(key)
            data = JSONDecoder().decode(json_data)

            # 1. filter the data based on the context score threshold - 0.0 is the default
            # 2. extract the gene symbols
            # 3. squeeze out any duplicate gene_symbols
            thresholded_data = [x for x in data if x[1] != 'NULL' and float(x[1]) < context_score_threshold]
            gene_list = map(lambda x: x[0], thresholded_data)
            gene_list = list(set(gene_list))
            final_data = [x for x in thresholded_data if lambda x: x[0] in gene_list]
            no_of_hits = len(final_data)
            if max_no_genes > 0:
                gene_score_list = sorted(final_data, key=lambda x: x[1], reverse=True)[0:max_no_genes]
            else:
                gene_score_list = sorted(final_data, key=lambda x: x[1], reverse=True)
        except KeyError:
            pass

    return no_of_hits, gene_score_list, gene_list
