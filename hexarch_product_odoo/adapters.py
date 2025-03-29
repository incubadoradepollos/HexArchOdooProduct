import xmlrpc.client

# from exceptions import ProductCreateException
from hexarch_product_core.models import CoreProduct
from hexarch_product_core.interfaces import IProductAdapter


class OdooProductAdapter(IProductAdapter):
    def __init__(self, url_odoo: str, db_odoo: str, user_odoo:str, password_odoo:str):
        # Autenticación
        common = xmlrpc.client.ServerProxy(f"{url_odoo}/xmlrpc/2/common")
        self.url_odoo = url_odoo
        self.db_odoo = db_odoo
        self.user_odoo = user_odoo
        self.password_odoo = password_odoo

        self.uid = common.authenticate(db_odoo, user_odoo, password_odoo, {})
        if not self.uid:
            print("Error de autenticación")
            exit()

        # Conexión a modelos
        self.odoo_clien = xmlrpc.client.ServerProxy(f"{url_odoo}/xmlrpc/2/object")        
        

    
    def get_product(self, id_product:int) -> CoreProduct:

        producto_odoo = self.odoo_clien.execute_kw(self.db_odoo, self.uid, self.password_odoo, 'product.template', 'search_read',
                [[['id', '=', id_product]]],  # Filtro de búsqueda
                {}  # Campos que queremos obtener
                )
        product = CoreProduct (
            id = producto_odoo["id"],
            name = producto_odoo["name"],
            price=producto_odoo["list_price"],
            barcode=producto_odoo["barcode"],
            default_code=producto_odoo["default_code"]
        )
        # Mostrar el resultado
        if producto_odoo:
            print("Producto encontrado:", producto_odoo)
            print("Producto 2 encontrado:", product)
        else:
            print(f"No se encontró un producto con ID {7}")
        
        return product

    def create_product(self, product: CoreProduct):

        tags_id = []
        for tag in product.tags:
            tags_id.append(self.get_or_create_tag_id(tag))

        product_id = self.odoo_clien.execute_kw(
            self.db_odoo, self.uid, self.password_odoo, 'product.template', 'create', [{
                'name': product.name,
                'type': 'consu',  # 'storable' para almacenable, 'consu' para consumible
                'list_price': product.price,  # Precio de venta
                'standard_price': product.price_cost,  # Precio de costo
                'default_code': product.default_code,  # Código interno
                'categ_id': 1,  # ID de la categoría interna del producto
                'public_categ_ids': product.categories,  # ID de la categoría de eCommerce (reemplazar con un ID real)
                'sale_ok': True,  # Disponible para la venta
                'website_published': True,  # Publicado en la tienda online
                'description': product.ia_descripcion,  #'SE PUEDE INCUIR EL TEXTO INICIAL DE LA IA',
                'description_sale': product.store_description, # 'DONDE ESTA UBICADO',
                'description_ecommerce': product.ecommerce_description, #'Descripcion para el ecomerce',
                'image_1920': product.images_base64[0],  # Aquí pasamos la imagen en formato Base64
                'product_tag_ids': tags_id
            }]
        )

        product.id = product_id
        return product
    
    def send_product(self,product: CoreProduct) -> CoreProduct:
        pass
        
    

    def get_or_create_tag_id(self, tag_name):
        
        tags =self.odoo_clien.execute_kw(
            self.db_odoo, self.uid, self.password_odoo, 'product.tag', 'search_read', 
            [[['name', '=', f"{tag_name}"]]], {'fields': ['id', 'name']})
        if tags:            
            return tags[0]['id']
        else:
            tag_id = self.odoo_clien.execute_kw(
                self.db_odoo, self.uid, self.password_odoo, 'product.tag', 'create', 
                [{'name': f"{tag_name}"}])            
            return tag_id        