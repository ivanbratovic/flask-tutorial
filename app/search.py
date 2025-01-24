from flask import current_app


def add_to_index(index, row_object):
    if not current_app.elasticsearch:
        return

    payload = {}
    searchable_fields = row_object.__searchable__

    for field in searchable_fields:
        payload[field] = getattr(row_object, field)

    current_app.elasticsearch.index(index=index, id=row_object.id, document=payload)


def remove_from_index(index, row_object):
    if not current_app.elasticsearch:
        return

    current_app.elasticsearch.delete(index=index, id=row_object.id)


def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return
    search = current_app.elasticsearch.search(
        index=index,
        query={"multi_match": {"query": query, "fields": ["*"]}},
        from_=(page - 1) * per_page,
        size=per_page,
    )
    ids = [hit["_id"] for hit in search["hits"]["hits"]]
    return ids, search['hits']['total']['value']