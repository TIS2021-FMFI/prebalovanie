# useful methods to be used in all apps

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def filtered_records(request, records_filter, paginate_by):
    # inspiracia: https://www.youtube.com/watch?v=G-Rct7Na0UQ
    list_filtered = records_filter.qs
    # paginacia  https://www.youtube.com/watch?v=N-PB-HMFmdo
    # pocet udajov na stranke https://stackoverflow.com/questions/57487336/change-value-for-paginate-by-on-the-fly
    p = Paginator(list_filtered, paginate_by)
    page = request.GET.get('page')

    try:
        complete_list = p.get_page(page)
    except PageNotAnInteger:
        complete_list = p.get_page(1)
    except EmptyPage:
        complete_list = p.get_page(1)
    return complete_list
