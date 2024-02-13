from db_utilities.DBcm import DBContextManager


def select(dbconfig: dict, _sql: str):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')

        cursor.execute(_sql)
        schema = [column[0] for column in cursor.description]
        result = cursor.fetchall()
    return result, schema



def insert(dbconfig: dict, _sql: str):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')

        cursor.execute(_sql)
    return 1

def select_dict(db_config: dict, _sql: str):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        else:
            cursor.execute(_sql)
            products = cursor.fetchall()
            if products:
                schema = [item[0] for item in cursor.description]
                products_dict = []
                for product in products:
                    products_dict.append(dict(zip(schema, product)))
                return products_dict
            else:
                return None


def insert_table(db_config: dict, _sql: str):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        else:
            cursor.execute(_sql)
            return None
