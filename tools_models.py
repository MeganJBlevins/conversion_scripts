from peewee import *

database = MySQLDatabase("dps_tools", host="13.58.139.127", port=3306, user="magento", passwd="jXJa29^GT9O4")

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class ActiveStatus(BaseModel):
    name = CharField()

    class Meta:
        table_name = 'active_status'

class Users(BaseModel):
    badge_id = CharField(null=True)
    created_at = DateTimeField(null=True)
    dept_id = IntegerField(constraints=[SQL("DEFAULT 1")])
    email = CharField(null=True)
    email_verified_at = DateTimeField(null=True)
    first_name = CharField()
    init_password = CharField(null=True)
    last_name = CharField(null=True)
    password = CharField()
    pin = CharField(null=True)
    remember_token = CharField(null=True)
    security_level = IntegerField(constraints=[SQL("DEFAULT 1")])
    shipworks_username = CharField(null=True)
    status = IntegerField(constraints=[SQL("DEFAULT 1")])
    updated_at = DateTimeField(null=True)
    dpsuser_id = IntegerField(null=True)
    pms_picker_id = IntegerField(null=True)
    picker_code = IntegerField(null=True)
    secondeyes_email = CharField(null=True)

    class Meta:
        table_name = 'users'

class Counters(BaseModel):
    name = CharField(null=True)
    email = CharField()
    password = CharField()
    email_verified_at = DateTimeField(null=True)
    updated_at = DateTimeField(null=True)
    remember_token = CharField(null=True)
    created_at = DateTimeField(null=True)
    updated_at = DateTimeField(null=True)
    

    class Meta:
        table_name = 'counters'

class Picks(BaseModel):
    actual_picked_orders = IntegerField(null=True)
    admin_login = IntegerField(constraints=[SQL("DEFAULT 0")])
    login = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    logout = DateTimeField(null=True)
    total_orders = IntegerField(null=True)
    user_id = IntegerField()

    class Meta:
        table_name = 'picks'

class Orders(BaseModel):
    increment_id = CharField()
    base_grand_total = DecimalField()
    billing_address_id = IntegerField()
    created_at = DateTimeField(null=True)
    customer_id = IntegerField(null=True)
    party_date = DateTimeField(null=True)
    pick = ForeignKeyField(column_name='pick_id', field='id', model=Picks, null=True)
    region = CharField(null=True)
    shipping_address_id = IntegerField()
    shipping_cost = DecimalField()
    shipping_description = CharField()
    status = CharField()
    sub_total = DecimalField()
    total_cost = DecimalField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'orders'

class Addresses(BaseModel):
    address = CharField()
    business_name = CharField(null=True)
    city = CharField()
    country = CharField()
    email = CharField()
    first_name = CharField()
    is_shipping = IntegerField(constraints=[SQL("DEFAULT 1")])
    last_name = CharField()
    order = ForeignKeyField(column_name='order_id', field='id', model=Orders, null=True)
    phone = CharField()
    region = CharField()
    type = CharField(constraints=[SQL("DEFAULT 'shipping'")])
    zip_code = CharField()

    class Meta:
        table_name = 'addresses'

class AmazonCaseCounts(BaseModel):
    count = IntegerField()
    created_at = DateTimeField(null=True)
    updated_at = DateTimeField(null=True)
    user = ForeignKeyField(column_name='user_id', field='id', model=Users)

    class Meta:
        table_name = 'amazon_case_counts'

class CycleCountAudits(BaseModel):
    aisle = CharField(null=True)
    count_correct = IntegerField(null=True)
    created_at = DateTimeField(null=True)
    new_qoh = IntegerField(null=True)
    old_qoh = IntegerField(null=True)
    product_id = IntegerField(null=True)
    schedule_id = IntegerField(null=True)
    sku = CharField(null=True)
    updated_at = DateTimeField(null=True)
    user = ForeignKeyField(column_name='user_id', field='id', model=Users, null=True)

    class Meta:
        table_name = 'cycle_count_audits'

class CycleCountSchedules(BaseModel):
    current = IntegerField()
    name = CharField(null=True)

    class Meta:
        table_name = 'cycle_count_schedules'

class CycleCountUpcErrors(BaseModel):
    comments = TextField(null=True)
    created_at = DateTimeField(null=True)
    not_in_system = IntegerField(null=True)
    pulled_shelf = IntegerField(null=True)
    qty_counted = IntegerField(null=True)
    status = IntegerField(null=True)
    upc = CharField()
    updated_at = DateTimeField(null=True)
    updated_by = ForeignKeyField(column_name='updated_by', field='id', model=Users, null=True)
    user = ForeignKeyField(backref='users_user_set', column_name='user_id', field='id', model=Users, null=True)

    class Meta:
        table_name = 'cycle_count_upc_errors'

class Locations(BaseModel):
    type = CharField()
    value = CharField()

    class Meta:
        table_name = 'locations'

class Migrations(BaseModel):
    batch = IntegerField()
    migration = CharField()

    class Meta:
        table_name = 'migrations'

class Vendors(BaseModel):
    account_id = CharField(null=True)
    address = CharField(null=True)
    city = CharField(null=True)
    contact_email = CharField(null=True)
    contact_name = CharField(null=True)
    contact_phone = CharField(null=True)
    country = CharField(null=True)
    name = CharField()
    state = CharField(null=True)
    vendor_phone = CharField(null=True)
    zip_code = CharField(null=True)

    class Meta:
        table_name = 'vendors'

class Products(BaseModel):
    active_status = IntegerField(null=True)
    created_at = DateTimeField(null=True)
    description = TextField(null=True)
    feed = CharField(null=True)
    image_url = CharField(null=True)
    is_live = IntegerField(null=True)
    name = CharField()
    price = DecimalField(null=True)
    sku = CharField()
    type = IntegerField(null=True)
    upc = CharField(null=True)
    updated_at = DateTimeField(null=True)
    vendor = CharField(null=True)
    vendor_uom = CharField(null=True)
    pinata = BooleanField(default=0)
    amazon_upc = CharField(null=True)

    class Meta:
        table_name = 'products'

class OrderItems(BaseModel):
    cost = DecimalField(null=True)
    order_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    parent_product_id = IntegerField(null=True)
    price = DecimalField()
    product_id = ForeignKeyField(column_name='product_id', constraints=[SQL("DEFAULT 0")], field='id', model=Products)
    product_type = CharField(constraints=[SQL("DEFAULT 'simple'")])
    qty = IntegerField()

    class Meta:
        table_name = 'order_items'

class OrdersCompleted(BaseModel):
    created_at = DateTimeField(null=True)
    order_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField(null=True)
    user = IntegerField(constraints=[SQL("DEFAULT 1")])
    scanned_by = CharField(null=True)
    class Meta:
        table_name = 'orders_completed'

class PasswordResets(BaseModel):
    created_at = DateTimeField(null=True)
    email = CharField(index=True)
    token = CharField()

    class Meta:
        table_name = 'password_resets'
        primary_key = False

class PurchaseOrders(BaseModel):
    created_at = DateTimeField(null=True)
    margin = DecimalField()
    purchase_order_number = CharField()
    receipt_at = DateTimeField(null=True)
    received = IntegerField(constraints=[SQL("DEFAULT 0")])
    reconciled = IntegerField(constraints=[SQL("DEFAULT 0")])
    status = CharField(constraints=[SQL("DEFAULT 'open'")])
    total_cost = DecimalField()
    total_items = IntegerField(constraints=[SQL("DEFAULT 0")])
    total_price = DecimalField(null=True)
    updated_at = DateTimeField(null=True)
    vendor = CharField()
    warehouse_id = IntegerField(constraints=[SQL("DEFAULT 1")])

    class Meta:
        table_name = 'purchase_orders'

class PurchaseOrderItems(BaseModel):
    active = IntegerField(constraints=[SQL("DEFAULT 1")])
    checked_in_amount = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField(null=True)
    order_qty = IntegerField()
    # product = ForeignKeyField(column_name='product_id', field='id', model=Products)
    product_id = IntegerField(null=True)
    sku = CharField(constraints=[SQL("DEFAULT 0")])
    product_price = DecimalField(null=True)
    purchase_order = ForeignKeyField(column_name='purchase_order_id', field='id', model=PurchaseOrders)
    total_cost = DecimalField(null=True)
    total_price = DecimalField(null=True)
    updated_at = DateTimeField(null=True)
    user = ForeignKeyField(column_name='user_id', field='id', model=Users, null=True)

    class Meta:
        table_name = 'purchase_order_items'

class Sessions(BaseModel):
    id = CharField(unique=True)
    ip_address = CharField(null=True)
    last_activity = IntegerField()
    payload = TextField()
    user_agent = TextField(null=True)
    user_id = IntegerField(null=True)

    class Meta:
        table_name = 'sessions'
        primary_key = False

class ShippingDetails(BaseModel):
    order_id = CharField()
    processed_date = DateTimeField(null=True)
    shipped_by = CharField()
    shipping_cost = DecimalField()
    shipping_fee = DecimalField()
    shipping_state = CharField(null=True)
    shipping_zipcode = CharField()

    class Meta:
        table_name = 'shipping_details'

class Tools(BaseModel):
    active = IntegerField()
    created_at = DateTimeField(null=True)
    name = CharField()
    slug = CharField()
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'tools'

class Trends(BaseModel):
    created_at = DateTimeField(null=True)
    ninety_day = IntegerField(constraints=[SQL("DEFAULT 0")])
    one_eighty_day = IntegerField(constraints=[SQL("DEFAULT 0")])
    prev_week = IntegerField(constraints=[SQL("DEFAULT 0")])
    product_id = IntegerField()
    seven_day = IntegerField(constraints=[SQL("DEFAULT 0")])
    thirty_day = IntegerField(constraints=[SQL("DEFAULT 0")])
    trend = IntegerField(null=True)
    sku = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'trends'

class UserReceivingCounts(BaseModel):
    count = IntegerField()
    created_at = DateTimeField(null=True)
    updated_at = DateTimeField(null=True)
    user_id = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'user_receiving_counts'

class WarehouseContacts(BaseModel):
    active = IntegerField()
    address = CharField()
    city = CharField()
    country = CharField()
    created_at = DateTimeField(null=True)
    email = CharField()
    first_name = CharField()
    last_name = CharField()
    primary_phone = CharField()
    secondary_phone = CharField()
    state = CharField()
    updated_at = DateTimeField(null=True)
    warehouse_id = IntegerField()
    zip_code = CharField()

    class Meta:
        table_name = 'warehouse_contacts'

class Warehouses(BaseModel):
    name = CharField()
    primary_contact = ForeignKeyField(column_name='primary_contact', field='id', model=WarehouseContacts, null=True)

    class Meta:
        table_name = 'warehouses'

class WarehouseProducts(BaseModel):
    created_at = DateTimeField(null=True)
    has_overstock = IntegerField(constraints=[SQL("DEFAULT 0")])
    ip_qty = IntegerField(null=True)
    # last_audit = IntegerField(null=True)
    name = CharField()
    order_up_to = IntegerField(null=True)
    os_aisle = CharField(null=True)
    os_bay = CharField(null=True)
    os_shelf = CharField(null=True)
    overstock_os_aisle = CharField(null=True)
    overstock_os_bay = CharField(null=True)
    overstock_os_shelf = CharField(null=True)
    plp = IntegerField(constraints=[SQL("DEFAULT 0")])
    product_id = IntegerField()
    qty = IntegerField(null=True)
    qty_on_hold = IntegerField(null=True)
    reorder_point = IntegerField(null=True)
    sku = CharField()
    # unit_markup = DecimalField(null=True)
    updated_at = DateTimeField(null=True)
    vendor_part_number = CharField(null=True)
    vendor_upc = CharField(null=True)
    warehouse = ForeignKeyField(column_name='warehouse_id', field='id', model=Warehouses)
    wh_cost = DecimalField(null=True)
    no_barcode = BooleanField(default=False)
    last_audit_id = IntegerField(null=True)

    class Meta:
        table_name = 'warehouse_products'

