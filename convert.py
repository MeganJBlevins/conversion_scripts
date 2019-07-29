from tools_models import (
    Vendors, Products, WarehouseProducts, CycleCountSchedules, PurchaseOrders,
    PurchaseOrderItems as toolsPOItems, Orders, Addresses,
    OrderItems, ShippingDetails, Picks, OrdersCompleted,
    UserReceivingCounts, CycleCountAudits
)
from magento_models import (
    VendorInfo, CatalogProductFlat2, DataWarehouse, CatalogProductIndexPrice,
    CataloginventoryStockItem, CycleCountAuditTrail, WarehouseOverstockCoordinates,
    CycleCountSchedule, PurchaseOrder, PurchaseOrderItems, SalesFlatOrder, SalesFlatOrderAddress,
    SalesFlatOrderItem, ShipworksShippingCosts, PmsPickerLogin, DpsusersReceivingcount, SecondEyesCompleted,
    CycleCountAuditTrail, CatalogProductEntityInt, CatalogProductEntity, CatalogProductEntityVarchar,
    CatalogProductEntityInt, CatalogProductIndexPrice,
)
import decimal
import datetime
from peewee import *
from random import randint

# Tools DB Max IDs
max_converted_vendor_id = Vendors.select(fn.MAX(Vendors.id)).scalar() or 0
max_converted_product_id = Products.select(fn.MAX(Products.id)).scalar() or 0
max_converted_warehouse_product_id = WarehouseProducts.select(fn.MAX(WarehouseProducts.id)).scalar() or 0
max_converted_cycle_count_schedules = CycleCountSchedules.select(fn.MAX(CycleCountSchedules.id)).scalar() or 0
max_converted_purchase_orders = PurchaseOrders.select(fn.MAX(PurchaseOrders.id)).scalar() or 0
max_converted_toolsPOItems = toolsPOItems.select(fn.MAX(toolsPOItems.id)).scalar() or 0
max_converted_order_id = Orders.select(fn.MAX(Orders.id)).scalar() or 0
max_converted_address_id = Addresses.select(fn.MAX(Addresses.id)).scalar() or 0
max_converted_order_item_id = OrderItems.select(fn.MAX(OrderItems.id)).scalar() or 0
max_converted_shipping_details = ShippingDetails.select(fn.MAX(ShippingDetails.order_id)).scalar() or 0
max_converted_picks = Picks.select(fn.MAX(Picks.id)).scalar() or 0
max_converted_orders_completed = OrdersCompleted.select(fn.MAX(OrdersCompleted.id)).scalar() or 0
max_converted_user_receiving_count = UserReceivingCounts.select(fn.MAX(UserReceivingCounts.id)).scalar() or 0
max_converted_cycle_count_audits = CycleCountAudits.select(fn.MAX(CycleCountAudits.id)).scalar() or 0
max_converted_products = WarehouseProducts.select(fn.MAX(WarehouseProducts.product_id)).scalar() or 0


# Magento DB Max IDs
max_vendor_id = VendorInfo.select(fn.MAX(VendorInfo.vendor_id)).scalar() or 0
max_catalog_product_id = CatalogProductFlat2.select(fn.MAX(CatalogProductFlat2.entity_id)).scalar() or 0
max_data_warehouse_id = DataWarehouse.select(fn.MAX(DataWarehouse.product_id)).scalar() or 0
max_cycle_count_schedule = CycleCountSchedule.select(fn.MAX(CycleCountSchedule.schedule_id)).scalar() or 0
max_purchase_orders = PurchaseOrder.select(fn.MAX(PurchaseOrder.id)).scalar() or 0
max_order_purchase_order_item_id = PurchaseOrderItems.select(fn.MAX(PurchaseOrderItems.id)).scalar() or 0
max_order_id = SalesFlatOrder.select(fn.MAX(SalesFlatOrder.entity_id)).scalar() or 0
max_address_id = SalesFlatOrderAddress.select(fn.MAX(SalesFlatOrderAddress.entity_id)).scalar() or 0
max_order_item_id = SalesFlatOrderItem.select(fn.MAX(SalesFlatOrderItem.item_id)).scalar() or 0
max_shipping_costs = ShipworksShippingCosts.select(fn.MAX(ShipworksShippingCosts.order_num)).scalar() or 0
max_pms_picker_login = PmsPickerLogin.select(fn.MAX(PmsPickerLogin.login_id)).scalar() or 0
max_secondeyes_completed = SecondEyesCompleted.select(fn.MAX(SecondEyesCompleted.id)).scalar() or 0
max_dps_user_receiving_count = DpsusersReceivingcount.select(fn.MAX(DpsusersReceivingcount.id)).scalar() or 0
max_cycle_count_audits = CycleCountAuditTrail.select(fn.MAX(CycleCountAuditTrail.id)).scalar() or 0
max_location_converted = WarehouseLocationMatrix.select(fn.MAX(WarehouseLocationMatrix.product_id)).scalar() or 0



# ========================================================================== #
# CONVERT VENDORS
# ========================================================================== #
if max_vendor_id > max_converted_vendor_id:
    vs = VendorInfo.select().where(VendorInfo.vendor_id > max_converted_vendor_id)
    for v in vs:
        new_vendor = {
            'id': v.vendor_id,
            'name': v.name,
            'contact_name': v.contact,
            'account_id': v.account_id,
            'address': v.address,
            'city': v.city,
            'state': v.state,
            'zip_code': v.zip or 0,
            'country': '',
            'vendor_phone': v.phone,
            'contact_phone': v.contact_phone,
            'contact_email': v.contact_email
        }
        # print(new_vendor)
        print("Creating vendor %s" % v.vendor_id)
        Vendors.create(**new_vendor)
else:
    print("All vendors converted!")

# ========================================================================== #
# CONVERT PRODUCTS
# ========================================================================== #
if max_catalog_product_id > max_converted_product_id:
    pfs = CatalogProductEntity.select().where(CatalogProductEntity.entity_id > max_converted_product_id)
    for pf in pfs: 
        print(pf.entity_id)
        try:
            product_name = CatalogProductEntityVarchar.select().where(CatalogProductEntityVarchar.entity_id == pf.entity_id, CatalogProductEntityVarchar.attribute_id == 71).get()
            product_image = CatalogProductEntityVarchar.select().where(CatalogProductEntityVarchar.entity_id == pf.entity_id, CatalogProductEntityVarchar.attribute_id == 85).get()
            product_description = CatalogProductEntityVarchar.select().where(CatalogProductEntityVarchar.entity_id == pf.entity_id, CatalogProductEntityVarchar.attribute_id == 84).get()
            product_amazon_upc = CatalogProductEntityVarchar.select().where(CatalogProductEntityVarchar.entity_id == pf.entity_id, CatalogProductEntityVarchar.attribute_id == 136).get()
        except: 
            pass
        
        try:
            product_is_live_obj = CatalogProductEntityInt.select().where(CatalogProductEntityInt.entity_id == pf.entity_id, CatalogProductEntityInt.attribute_id == 133).get()
            product_is_live = product_is_live_obj.value
        except:
            product_is_live = 0

        try:
            product_feed_obj = CatalogProductEntityInt.select().where(CatalogProductEntityInt.entity_id == pf.entity_id, CatalogProductEntityInt.attribute_id == 177).get()
            product_feed = product_feed_obj.value
        except:
            product_feed = 0
        try:
            price_obj = CatalogProductIndexPrice.select().where(CatalogProductIndexPrice.entity_id == pf.entity_id, CatalogProductIndexPrice.customer_group_id == 1).get()
            price_final = price_obj.final_price
        except:
            price_final = 0

        try:
            pinata_obj = CatalogProductEntityInt.select().where(CatalogProductEntityInt.entity_id == pf.entity_id, CatalogProductEntityInt.attribute_id == 148).get()
            pinata = pinata_obj.value
        except:
            pinata = 0

        try:
            warehouse = DataWarehouse.select().where(DataWarehouse.sku == pf.sku).get()
        except:
            warehouse = None

        if warehouse is not None:
            upc = warehouse.upc
            vendor_name = warehouse.vendor
            print(vendor_name)
            # vendor = VendorInfo.select().where(VendorInfo.name == vendor_name).get()
            if warehouse.vendor_uom == '1o0':
                uom = 100
            else:
                uom = warehouse.vendor_uom

            active = warehouse.active_status
        else:
            upc = None
            vendor_name = None
            uom = 1
            active = 2
           
        new_product = {
            'id': pf.entity_id,
            'sku': pf.sku,
            'name': product_name.value,
            'description': product_description.value,
            'type': pf.type_id,
            'upc': upc,
            'image_url': product_image.value,
            'vendor': vendor_name,
            'vendor_uom': uom,
            'active_status': active,
            'is_live': product_is_live or 1,
            'feed': product_feed,
            'price': price_final,
            'pinata': pinata or 0,
            'amazon_upc': product_amazon_upc.value
        }   

        print("Creating product %s" % pf.entity_id)
        Products.create(**new_product)

else:
    print("All products converted!")

# ========================================================================== #
# CONVERT WAREHOUSE PRODUCTS
# ========================================================================== #
if max_data_warehouse_id > max_converted_warehouse_product_id:
    print('running script')
    dws = DataWarehouse.select().where(DataWarehouse.product_id > max_converted_warehouse_product_id)
    # dws = DataWarehouse.select().where(DataWarehouse.sku == '200336000000_npl425955')
    for dw in dws:
        try:
            vendor = Vendors.select().where(Vendors.name == dw.vendor).get()
            vendor_id = vendor.id
        except:
            new_vendor = {
                'name': dw.vendor,
                'contact_name': '',
                'account_id': 0,
                'address': '',
                'city': '',
                'state': '',
                'zip_code': 0,
                'country': '',
                'vendor_phone': '',
                'contact_phone': '',
                'contact_email': ''
            }
            vendor = Vendors.create(**new_vendor)
            vendor_id = vendor.id

        try:
            woc = WarehouseOverstockCoordinates.select().where(WarehouseOverstockCoordinates.upc == dw.upc).get()
            overstock = True
            overstock_os_aisle = woc.x
            overstock_os_bay = woc.y
            overstock_os_shelf = woc.shelf
        except:
            overstock = False
            overstock_os_aisle = ''
            overstock_os_bay = ''
            overstock_os_shelf = ''

        try:
            ccat = CycleCountAuditTrail.select().where(CycleCountAuditTrail.sku == dw.sku).order_by(CycleCountAuditTrail.timestamp.desc()).first()
            the_last_audit = ccat.id
        except:
            the_last_audit = None

        try:
            product_qty = CataloginventoryStockItem.select().where(CataloginventoryStockItem.product_id == dw.product_id).get()
            qty = product_qty.qty
        except:
            product_qty = None

        new_product = {
            'product_id': dw.product_id,
            'price': dw.price,
            'sku': dw.sku,
            'name': dw.name,
            'vendor_upc': dw.vendor_upc,
            'vendor_part_number': dw.vendor_num,
            'ip_qty': dw.ip_qty,
            'wh_cost': dw.vendor_cost,
            'reorder_point': dw.reorder_point,
            'order_up_to': dw.order_up_to,
            'os_aisle': dw.os_aisle,
            'os_bay': dw.os_bay,
            'os_shelf': dw.os_shelf,
            'has_overstock': overstock,
            'overstock_os_aisle': overstock_os_aisle,
            'overstock_os_bay': overstock_os_bay,
            'overstock_os_shelf': overstock_os_shelf,
            'plp': dw.plp or 0,
            'qty': qty,
            'qty_on_hold': 0,
            'last_audit_id': the_last_audit,
            'warehouse_id': 1,
        }   
        print("Creating warehouse product %s" % dw.product_id)
        product = WarehouseProducts.create(**new_product)
    
else:
    print("All warehouse products converted!")


# ========================================================================== #
# CONVERT Cycle Counts Audits
# ========================================================================== #
if max_cycle_count_schedule > max_converted_cycle_count_schedules:
    print('cycle counts converting')
    ccas = CycleCountSchedule.select().where(CycleCountSchedule.schedule_id > max_converted_cycle_count_schedules)
    for ca in ccas:
        new_cycle_count_schedule = {
            'id': ca.schedule_id,
            'name': ca.name,
            'current': ca.current,
        }
        print("Adding cycle count schedule %s" % ca.schedule_id)
        CycleCountSchedules.create(**new_cycle_count_schedule)
else:
    print("All cycle count schedules converted!")


# ========================================================================== #
# CONVERT PURCHASE ORDERS
# ========================================================================== #
if max_purchase_orders > max_converted_purchase_orders:
    po = PurchaseOrder.select().where(PurchaseOrder.id > max_converted_purchase_orders)
    for p in po:
        if p.receipt_date != None:
            received = 1
        else:
            received = 0

        try:
            vendor = Vendors.select().where(Vendors.name == p.vendor_id).get()
            vendor_id = vendor.id
        except:
            new_vendor = {
                'name': p.vendor_id,
                'contact_name': '',
                'account_id': 0,
                'address': '',
                'city': '',
                'state': '',
                'zip_code': 0,
                'country': '',
                'vendor_phone': '',
                'contact_phone': '',
                'contact_email': ''
            }
            vendor = Vendors.create(**new_vendor)
            vendor_id = vendor.id

        new_purchase_order = {
            'id': p.id,
            'purchase_order_number': p.id,
            'status': p.status,
            'vendor_id': p.vendor_id,
            'warehouse_id': 1,
            'total_cost': p.total_cost,
            'total_price': 0,
            'total_items': p.total_items,
            'received': received,
            'reconciled': p.reconciled or 0,
            'receipt_at': p.receipt_date,
            'margin': 0,
        }
        print("Creating purchase order %s" % p.id)
        PurchaseOrders.create(**new_purchase_order)

else:
    print("All purchase orders converted!")

# ========================================================================== #
# CONVERT PURCHASE ORDER ITEMS
# ========================================================================== #
if max_order_purchase_order_item_id > max_converted_toolsPOItems:
    print('purchase order items converting')
    poi = PurchaseOrderItems.select().where(PurchaseOrderItems.id > max_converted_toolsPOItems)
    # poi = PurchaseOrderItems.select().where(PurchaseOrderItems.id == 633756)
    for oi in poi:

        product_price = None;
        try:
            product = Products.select().where(Products.sku == oi.sku).get()
        except DoesNotExist:
            product = None

        if product is not None:
            product_price = product.price
            product_id = product.id or 0
            total_price = product_price * int(product.vendor_uom)
        else:
            product_id = 0
            product_price = 0
            total_price = 0

        new_purchase_order_item = {
            'id': oi.id,
            'purchase_order_id': oi.po_id,
            'product_id': product_id,
            'sku': oi.sku,
            'order_qty': oi.vendor_qty,
            'checked_in_amount': oi.qty_received,
            'user_id': None,
            'active': 1,
            'product_price': product_price,
            'total_cost': oi.cost,
            'total_price': total_price,
        }
        print("Adding purchase Order Item %s" % oi.sku)
        # try:
        toolsPOItems.create(**new_purchase_order_item)
        # except:
        #     pass
else:
    print("All purchase order items converted!")


# ========================================================================== #
# CONVERT ORDERS & ADDRESSES
# ========================================================================== #
print('running convertOrders.py')
if max_order_id > max_converted_order_id:
    os = SalesFlatOrder.select().where(SalesFlatOrder.entity_id > max_converted_order_id)
    # os = SalesFlatOrder.select().where(SalesFlatOrder.increment_id == '100118731')

    for o in os.iterator():

        ship = ShipworksShippingCosts.select().where(ShipworksShippingCosts.order_num == o.increment_id).first()
        increment_id = o.increment_id

        if ship is not None:

            if ship.processed_date == '0000-00-00':
                processed_date = None
            else:
                processed_date = ship.processed_date

            new_shipping_details = {
                'order_id': increment_id,
                'processed_date': processed_date,
                'shipping_cost': ship.shipping_cost,
                'shipping_fee': ship.shipping_fee,
                'shipped_by': ship.shipping_service,
                'shipping_state': ship.shipping_state,
                'shipping_zipcode': ship.shipping_zipcode,
            }
            print('Creating shipping detail %s'  % increment_id)
            ShippingDetails.create(**new_shipping_details)
        else:
            print('shipping details not created for %s' % increment_id)
            pass

        if o.party_date is isinstance(o.party_date, datetime.date):
            party_date = o.party_date
        else:
            party_date = None
        oas = SalesFlatOrderAddress.select().where(SalesFlatOrderAddress.parent == o)
        region = ''
        for oa in oas:
            region = oa.region
        new_order = {
            'id': o.entity_id,
            'increment_id': increment_id,
            'region': region,
            'sub_total': o.base_subtotal,
            'shipping_cost': o.shipping_amount or 0,
            'status': o.status or 1,
            'customer_id': o.customer_id,
            'base_grand_total': o.base_grand_total,
            'shipping_description': o.shipping_description or '',
            'billing_address_id': o.billing_address_id,
            'shipping_address_id': o.shipping_address_id,
            'shipping_amount': o.shipping_amount,
            'party_date': party_date,
            'created_at': o.created_at,
            'updated_at': o.updated_at
        }
        
        print("Creating order %s" % o.entity_id)
        Orders.create(**new_order)
        for oa in oas:
            addy = None
            addy = Addresses.select().where(Addresses.id == oa.entity_id)

            if addy is not None:
                new_order_address = {
                    'id': oa.entity_id,
                    'address': oa.street or '',
                    'business_name': oa.company or '',
                    'city': oa.city or '',
                    'country': oa.country_id or '',
                    'email': oa.email or '',
                    'first_name': oa.firstname or '',
                    'is_active': True,
                    'last_name': oa.lastname or '',
                    'order_id': o.entity_id,
                    'phone': oa.telephone or '',
                    'region': oa.region or '',
                    'type': oa.address_type or '',
                    'zip_code': oa.postcode or 0
                }
                print("Creating address %s" % oa.entity_id)
                Addresses.create(**new_order_address)
            else:
                pass
else:
    print("All orders converted!")

max_order_item_id = SalesFlatOrderItem.select(fn.MAX(SalesFlatOrderItem.item_id)).scalar() or 0

# ========================================================================== #
# CONVERT ORDER ITEMS
# ========================================================================== #
if max_order_item_id > max_converted_order_item_id:
    print('order items converting')
    ois = SalesFlatOrderItem.select().where(SalesFlatOrderItem.item_id > max_converted_order_item_id)
    for oi in ois.iterator():
        try:
            dw = DataWarehouse.select().where(DataWarehouse.product_id == oi.product_id).get()
        except DoesNotExist:
            dw = None

        new_order_item = {
            'id': oi.item_id,
            'order_id': oi.order_id,
            'qty': oi.qty_ordered,
            'cost': dw.vendor_cost if dw else 0,
            'price': oi.price,
            'product_id': oi.product_id,
            'parent_product_id': oi.parent_item_id,
            'product_type': oi.product_type,
        }
        print("Adding order_item %s" % oi.item_id)
        # try:
        OrderItems.create(**new_order_item)
        # except:
        #     pass
else:
    print("All order items converted!")

# ========================================================================== #
# CONVERT Picks
# ========================================================================== #
if max_pms_picker_login > max_converted_picks:
    ppl = PmsPickerLogin.select().where(PmsPickerLogin.login_id > max_converted_picks)
    for pp in ppl:
            
        new_pick = {
            'id': pp.login_id,
            'user_id': pp.picker_id,
            'login': pp.login,    
            'logout': pp.logout,
            'total_orders': pp.total_orders or 0,
            'actual_picked_orders': pp.actual_picked_orders or 0,
            'admin_login': pp.admin_login or 0
            
        }

        print("Creating pick %s" % pp.login_id)
        Picks.create(**new_pick)
else:
    print("All users converted")


# ========================================================================== #
# CONVERT ORDERS COMPLETED
# ========================================================================== #

if max_secondeyes_completed > max_converted_orders_completed:
    print('Orders Completed Converting')
    sec = SecondEyesCompleted.select().where(SecondEyesCompleted.id > max_converted_orders_completed)
    for oc in sec:

        new_order_completed = {
            'id': oc.id,
            'order_number': oc.order_number,
            'user_id': None,
            'scanned_by': oc.scanned_by,
            'created_at': oc.timestamp,
        }
        print("Adding order_completed %s" % oc.id)
        OrdersCompleted.create(**new_order_completed)

else:
    print("All orders completed converted!")


# ========================================================================== #
# CONVERT USER RECEIVING COUNTS
# ========================================================================== #

if max_dps_user_receiving_count > max_converted_user_receiving_count:
    print('User Receiving Counts Converting')
    urc = DpsusersReceivingcount.select().where(DpsusersReceivingcount.id > max_converted_user_receiving_count)
    for ur in urc:

        new_user_receving_count = {
            'id': ur.id,
            'user_id': ur.user_id,
            'count': ur.count,
            'created_at': ur.timestamp,
        }
        print("Adding user receiving count %s" % ur.id)
        # try:
        UserReceivingCounts.create(**new_user_receving_count)
        # except:
        #     pass
else:
    print("All user receiving counts converted!")

# ========================================================================== #
# CONVERT Locations
# ========================================================================== #
if max_converted_products > max_location_converted:
    prod = WarehouseProducts.select()
    for p in prod.iterator():
        item = WarehouseLocationMatrix.select().where(WarehouseLocationMatrix.product_id == p.product_id).first()
        if item is not None:
            location = WarehouseLocations.select().where(WarehouseLocations.location_id == item.location_id).first()
            aisleQuery = WarehouseProducts.update(os_aisle=location.aisle).where(WarehouseProducts.product_id == p.product_id)
            bayQuery = WarehouseProducts.update(os_bay=location.bay).where(WarehouseProducts.product_id == p.product_id)
            shelfQuery = WarehouseProducts.update(os_shelf=location.shelf).where(WarehouseProducts.product_id == p.product_id)
            a = aisleQuery.execute()
            b = bayQuery.execute()
            s = shelfQuery.execute()
            print('{} location updated'.format(p.product_id))
        else:
            pass
else:
    print("All locations converted!")