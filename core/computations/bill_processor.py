"""
Core computation logic for bill processing - extracted from streamlit_app.py
This module contains the core business logic that should not be modified.
"""
import pandas as pd
import numpy as np
from datetime import datetime, date

def safe_float(value, default=0.0):
    """Safely convert a value to float with proper error handling"""
    try:
        if value is None:
            return default
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            # Clean the string
            cleaned = value.strip().replace(',', '').replace(' ', '')
            # Handle empty string
            if cleaned == '':
                return default
            # Try to convert
            return float(cleaned)
        return default
    except (ValueError, TypeError):
        return default

def number_to_words(number):
    """Convert number to words using num2words"""
    try:
        from num2words import num2words
        return num2words(int(number), lang="en_IN").title()
    except:
        return str(number)

def process_bill(ws_wo, ws_bq, ws_extra, premium_percent, premium_type):
    """
    Process bill data from Excel sheets
    
    Args:
        ws_wo: Work Order worksheet
        ws_bq: Bill Quantity worksheet
        ws_extra: Extra Items worksheet
        premium_percent: Tender premium percentage
        premium_type: "above" or "below"
    
    Returns:
        tuple: (first_page_data, last_page_data, deviation_data, extra_items_data, note_sheet_data)
    """
    first_page_data = {"header": [], "items": [], "totals": {}}
    last_page_data = {"payable_amount": 0, "amount_words": ""}
    deviation_data = {"items": [], "summary": {}}
    extra_items_data = {"items": []}
    note_sheet_data = {"notes": []}

    # Header (A1:G19) only — matching actual data range
    header_data = ws_wo.iloc[:19, :7].replace(np.nan, "").values.tolist()

    # Ensure all dates are formatted as date-only strings
    for i in range(len(header_data)):
        for j in range(len(header_data[i])):
            val = header_data[i][j]
            if isinstance(val, (pd.Timestamp, datetime, date)):
                header_data[i][j] = val.strftime("%d-%m-%Y")

    first_page_data["header"] = header_data

    # Work Order items
    last_row_wo = ws_wo.shape[0]
    for i in range(21, last_row_wo):
        qty_raw = ws_bq.iloc[i, 3] if i < ws_bq.shape[0] and pd.notnull(ws_bq.iloc[i, 3]) else None
        rate_raw = ws_wo.iloc[i, 4] if pd.notnull(ws_wo.iloc[i, 4]) else None

        qty = 0
        if isinstance(qty_raw, (int, float)):
            qty = float(qty_raw)
        elif isinstance(qty_raw, str):
            cleaned_qty = qty_raw.strip().replace(',', '').replace(' ', '')
            # Handle empty string case
            if cleaned_qty == '':
                qty = 0
            else:
                try:
                    qty = float(cleaned_qty)
                except ValueError:
                    qty = 0

        rate = 0
        if isinstance(rate_raw, (int, float)):
            rate = float(rate_raw)
        elif isinstance(rate_raw, str):
            cleaned_rate = rate_raw.strip().replace(',', '').replace(' ', '')
            # Handle empty string case
            if cleaned_rate == '':
                rate = 0
            else:
                try:
                    rate = float(cleaned_rate)
                except ValueError:
                    rate = 0

        # Check if rate is blank or zero - if so, only populate S.No., Item of *, and Remarks
        if rate is None or rate == 0:
            item = {
                "serial_no": str(ws_wo.iloc[i, 0]) if pd.notnull(ws_wo.iloc[i, 0]) else "",
                "description": str(ws_wo.iloc[i, 1]) if pd.notnull(ws_wo.iloc[i, 1]) else "",
                "unit": "",  # Leave blank
                "quantity": "",  # Leave blank
                "quantity_since_last": "",  # Leave blank
                "quantity_upto_date": "",  # Leave blank
                "rate": "",  # Leave blank
                "remark": str(ws_wo.iloc[i, 6]) if pd.notnull(ws_wo.iloc[i, 6]) else "",
                "amount": "",  # Leave blank
                "amount_previous": "",  # Leave blank
                "is_divider": False
            }
        else:
            item = {
                "serial_no": str(ws_wo.iloc[i, 0]) if pd.notnull(ws_wo.iloc[i, 0]) else "",
                "description": str(ws_wo.iloc[i, 1]) if pd.notnull(ws_wo.iloc[i, 1]) else "",
                "unit": str(ws_wo.iloc[i, 2]) if pd.notnull(ws_wo.iloc[i, 2]) else "",
                "quantity": qty,
                "quantity_since_last": qty,  # For template compatibility
                "quantity_upto_date": qty,   # For template compatibility
                "rate": rate,
                "remark": str(ws_wo.iloc[i, 6]) if pd.notnull(ws_wo.iloc[i, 6]) else "",
                "amount": round(qty * rate) if qty and rate else 0,
                "amount_previous": round(qty * rate) if qty and rate else 0,  # For template compatibility
                "is_divider": False
            }
        first_page_data["items"].append(item)

    # Extra Items divider
    first_page_data["items"].append({
        "description": "Extra Items (With Premium)",
        "bold": True,
        "underline": True,
        "amount": 0,
        "amount_previous": 0,
        "quantity": 0,
        "quantity_since_last": 0,
        "quantity_upto_date": 0,
        "rate": 0,
        "serial_no": "",
        "unit": "",
        "remark": "",
        "is_divider": True
    })

    # Extra Items
    last_row_extra = ws_extra.shape[0]
    for j in range(6, last_row_extra):
        qty_raw = ws_extra.iloc[j, 3] if pd.notnull(ws_extra.iloc[j, 3]) else None
        rate_raw = ws_extra.iloc[j, 5] if pd.notnull(ws_extra.iloc[j, 5]) else None

        qty = 0
        if isinstance(qty_raw, (int, float)):
            qty = float(qty_raw)
        elif isinstance(qty_raw, str):
            cleaned_qty = qty_raw.strip().replace(',', '').replace(' ', '')
            # Handle empty string case
            if cleaned_qty == '':
                qty = 0
            else:
                try:
                    qty = float(cleaned_qty)
                except ValueError:
                    qty = 0

        rate = 0
        if isinstance(rate_raw, (int, float)):
            rate = float(rate_raw)
        elif isinstance(rate_raw, str):
            cleaned_rate = rate_raw.strip().replace(',', '').replace(' ', '')
            # Handle empty string case
            if cleaned_rate == '':
                rate = 0
            else:
                try:
                    rate = float(cleaned_rate)
                except ValueError:
                    rate = 0

        # Check if rate is blank or zero - if so, only populate S.No., Item of *, and Remarks
        if rate is None or rate == 0:
            item = {
                "serial_no": str(ws_extra.iloc[j, 0]) if pd.notnull(ws_extra.iloc[j, 0]) else "",
                "description": str(ws_extra.iloc[j, 2]) if pd.notnull(ws_extra.iloc[j, 2]) else "",
                "unit": "",  # Leave blank
                "quantity": "",  # Leave blank
                "quantity_since_last": "",  # Leave blank
                "quantity_upto_date": "",  # Leave blank
                "rate": "",  # Leave blank
                "remark": str(ws_extra.iloc[j, 1]) if pd.notnull(ws_extra.iloc[j, 1]) else "",
                "amount": "",  # Leave blank
                "amount_previous": "",  # Leave blank
                "is_divider": False
            }
        else:
            item = {
                "serial_no": str(ws_extra.iloc[j, 0]) if pd.notnull(ws_extra.iloc[j, 0]) else "",
                "description": str(ws_extra.iloc[j, 2]) if pd.notnull(ws_extra.iloc[j, 2]) else "",
                "unit": str(ws_extra.iloc[j, 4]) if pd.notnull(ws_extra.iloc[j, 4]) else "",
                "quantity": qty,
                "quantity_since_last": qty,  # For template compatibility
                "quantity_upto_date": qty,   # For template compatibility
                "rate": rate,
                "remark": str(ws_extra.iloc[j, 1]) if pd.notnull(ws_extra.iloc[j, 1]) else "",
                "amount": round(qty * rate) if qty and rate else 0,
                "amount_previous": round(qty * rate) if qty and rate else 0,  # For template compatibility
                "is_divider": False
            }
        first_page_data["items"].append(item)
        extra_items_data["items"].append(item.copy())  # Copy for standalone Extra Items

    # Totals
    data_items = [item for item in first_page_data["items"] if not item.get("is_divider", False)]
    total_amount = round(sum(safe_float(item.get("amount", 0)) for item in data_items))
    premium_amount = round(total_amount * (premium_percent / 100) if premium_type == "above" else -total_amount * (premium_percent / 100))
    payable_amount = round(safe_float(total_amount) + safe_float(premium_amount))

    first_page_data["totals"] = {
        "grand_total": total_amount,
        "premium": {"percent": premium_percent / 100, "type": premium_type, "amount": premium_amount},
        "payable": payable_amount
    }

    try:
        extra_items_start = next(i for i, item in enumerate(first_page_data["items"]) if item.get("description") == "Extra Items (With Premium)")
        extra_items = [item for item in first_page_data["items"][extra_items_start + 1:] if not item.get("is_divider", False)]
        extra_items_sum = round(sum(safe_float(item.get("amount", 0)) for item in extra_items))
        extra_items_premium = round(extra_items_sum * (premium_percent / 100) if premium_type == "above" else -extra_items_sum * (premium_percent / 100))
        first_page_data["totals"]["extra_items_sum"] = extra_items_sum + extra_items_premium
    except StopIteration:
        first_page_data["totals"]["extra_items_sum"] = 0

    # Last Page
    last_page_data = {"payable_amount": payable_amount, "amount_words": number_to_words(payable_amount)}

    # Deviation Statement
    work_order_total = 0
    executed_total = 0
    overall_excess = 0
    overall_saving = 0
    for i in range(21, last_row_wo):
        qty_wo_raw = ws_wo.iloc[i, 3] if pd.notnull(ws_wo.iloc[i, 3]) else None
        rate_raw = ws_wo.iloc[i, 4] if pd.notnull(ws_wo.iloc[i, 4]) else None
        qty_bill_raw = ws_bq.iloc[i, 3] if i < ws_bq.shape[0] and pd.notnull(ws_bq.iloc[i, 3]) else None

        qty_wo = 0
        if isinstance(qty_wo_raw, (int, float)):
            qty_wo = float(qty_wo_raw)
        elif isinstance(qty_wo_raw, str):
            cleaned_qty_wo = qty_wo_raw.strip().replace(',', '').replace(' ', '')
            # Handle empty string case
            if cleaned_qty_wo == '':
                qty_wo = 0
            else:
                try:
                    qty_wo = float(cleaned_qty_wo)
                except ValueError:
                    qty_wo = 0

        rate = 0
        if isinstance(rate_raw, (int, float)):
            rate = float(rate_raw)
        elif isinstance(rate_raw, str):
            cleaned_rate = rate_raw.strip().replace(',', '').replace(' ', '')
            # Handle empty string case
            if cleaned_rate == '':
                rate = 0
            else:
                try:
                    rate = float(cleaned_rate)
                except ValueError:
                    rate = 0

        qty_bill = 0
        if isinstance(qty_bill_raw, (int, float)):
            qty_bill = float(qty_bill_raw)
        elif isinstance(qty_bill_raw, str):
            cleaned_qty_bill = qty_bill_raw.strip().replace(',', '').replace(' ', '')
            # Handle empty string case
            if cleaned_qty_bill == '':
                qty_bill = 0
            else:
                try:
                    qty_bill = float(cleaned_qty_bill)
                except ValueError:
                    qty_bill = 0

        amt_wo = round(qty_wo * rate)
        amt_bill = round(qty_bill * rate)
        excess_qty = qty_bill - qty_wo if qty_bill > qty_wo else 0
        excess_amt = round(excess_qty * rate) if excess_qty > 0 else 0
        saving_qty = qty_wo - qty_bill if qty_bill < qty_wo else 0
        saving_amt = round(saving_qty * rate) if saving_qty > 0 else 0

        # Check if rate is blank or zero - if so, only populate Item No.
        if rate is None or rate == 0:
            item = {
                "serial_no": str(ws_wo.iloc[i, 0]) if pd.notnull(ws_wo.iloc[i, 0]) else "",
                "description": str(ws_wo.iloc[i, 1]) if pd.notnull(ws_wo.iloc[i, 1]) else "",  # Populate Description* for zero rate
                "unit": "",  # Leave blank as per specification
                "qty_wo": "",  # Leave blank as per specification
                "rate": "",  # Leave blank as per specification
                "amt_wo": "",  # Leave blank as per specification
                "qty_bill": "",  # Leave blank as per specification
                "amt_bill": "",  # Leave blank as per specification
                "excess_qty": "",  # Leave blank as per specification
                "excess_amt": "",  # Leave blank as per specification
                "saving_qty": "",  # Leave blank as per specification
                "saving_amt": "",  # Leave blank as per specification
                "remark": str(ws_wo.iloc[i, 6]) if pd.notnull(ws_wo.iloc[i, 6]) else ""  # Populate Remark for zero rate
            }
            # Don't add to totals when rate is zero
            deviation_item_amt_wo = 0
            deviation_item_amt_bill = 0
            deviation_item_excess_amt = 0
            deviation_item_saving_amt = 0
        else:
            # For non-zero rate items, use just the main description like the original
            full_description = str(ws_wo.iloc[i, 1]) if pd.notnull(ws_wo.iloc[i, 1]) else ""
            
            item = {
                "serial_no": str(ws_wo.iloc[i, 0]) if pd.notnull(ws_wo.iloc[i, 0]) else "",
                "description": full_description,
                "unit": str(ws_wo.iloc[i, 2]) if pd.notnull(ws_wo.iloc[i, 2]) else "",
                "qty_wo": qty_wo,
                "rate": rate,
                "amt_wo": amt_wo,
                "qty_bill": qty_bill,
                "amt_bill": amt_bill,
                "excess_qty": excess_qty,
                "excess_amt": excess_amt,
                "saving_qty": saving_qty,
                "saving_amt": saving_amt,
                "remark": str(ws_wo.iloc[i, 6]) if pd.notnull(ws_wo.iloc[i, 6]) else ""
            }
            # Add to totals when rate is valid
            deviation_item_amt_wo = amt_wo
            deviation_item_amt_bill = amt_bill
            deviation_item_excess_amt = excess_amt
            deviation_item_saving_amt = saving_amt

        deviation_data["items"].append(item)
        work_order_total += deviation_item_amt_wo
        executed_total += deviation_item_amt_bill
        overall_excess += deviation_item_excess_amt
        overall_saving += deviation_item_saving_amt

    # Deviation Summary
    tender_premium_f = round(safe_float(work_order_total) * (premium_percent / 100) if premium_type == "above" else -safe_float(work_order_total) * (premium_percent / 100))
    tender_premium_h = round(safe_float(executed_total) * (premium_percent / 100) if premium_type == "above" else -safe_float(executed_total) * (premium_percent / 100))
    tender_premium_j = round(safe_float(overall_excess) * (premium_percent / 100) if premium_type == "above" else -safe_float(overall_excess) * (premium_percent / 100))
    tender_premium_l = round(safe_float(overall_saving) * (premium_percent / 100) if premium_type == "above" else -safe_float(overall_saving) * (premium_percent / 100))
    grand_total_f = round(safe_float(work_order_total) + safe_float(tender_premium_f))
    grand_total_h = round(safe_float(executed_total) + safe_float(tender_premium_h))
    grand_total_j = round(safe_float(overall_excess) + safe_float(tender_premium_j))
    grand_total_l = round(safe_float(overall_saving) + safe_float(tender_premium_l))
    net_difference = round(safe_float(grand_total_h) - safe_float(grand_total_f))

    deviation_data["summary"] = {
        "work_order_total": round(work_order_total),
        "executed_total": round(executed_total),
        "overall_excess": round(overall_excess),
        "overall_saving": round(overall_saving),
        "premium": {"percent": premium_percent / 100, "type": premium_type},
        "tender_premium_f": tender_premium_f,
        "tender_premium_h": tender_premium_h,
        "tender_premium_j": tender_premium_j,
        "tender_premium_l": tender_premium_l,
        "grand_total_f": grand_total_f,
        "grand_total_h": grand_total_h,
        "grand_total_j": grand_total_j,
        "grand_total_l": grand_total_l,
        "net_difference": net_difference
    }

    return first_page_data, last_page_data, deviation_data, extra_items_data, note_sheet_data