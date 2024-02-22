# from flask_jsonpify import jsonify
# from flask import request
#
# from app import app, db
# from app.api.v1.uam.uam_utils import *
# from app.middleware import token_required
#
#
# @app.route("/getSNTC", methods=["GET"])
# @token_required
# def getSntc(user_data):
#     try:
#         sntcList = []
#         results = SNTC_TABLE.query.filter(
#             SNTC_TABLE.pn_code != "" and SNTC_TABLE.pn_code != "N/A"
#         ).all()
#
#         for sntc in results:
#             sntcDataDict = {}
#
#             sntcDataDict["sntc_id"] = sntc.sntc_id
#             sntcDataDict["pn_code"] = sntc.pn_code
#             sntcDataDict["hw_eos_date"] = FormatDate(sntc.hw_eos_date)
#             sntcDataDict["hw_eol_date"] = FormatDate(sntc.hw_eol_date)
#             sntcDataDict["sw_eos_date"] = FormatDate(sntc.sw_eos_date)
#             sntcDataDict["sw_eol_date"] = FormatDate(sntc.sw_eol_date)
#             sntcDataDict["manufacturer_date"] = FormatDate(sntc.manufacture_date)
#             sntcDataDict["creation_date"] = sntc.creation_date
#             sntcDataDict["modification_date"] = sntc.modification_date
#
#             sntcList.append(sntcDataDict)
#         return jsonify(sntcList), 200
#     except Exception:
#         traceback.print_exc()
#         return "Exception Occurred While SNTC GET", 500
#
#
# @app.route("/syncFromInventory", methods=["GET"])
# @token_required
# def SyncFromInventory(user_data):
#     try:
#         queryString = f"SELECT DISTINCT(pn_code) FROM uam_device_table WHERE pn_code NOT IN (SELECT pn_code FROM sntc_table) UNION select distinct(pn_code) from board_table where pn_code not in (select pn_code from sntc_table) UNION select distinct pn_code from subboard_table where pn_code not in (select pn_code from sntc_table) UNION SELECT DISTINCT(pn_code) FROM sfp_table WHERE pn_code NOT IN (SELECT pn_code FROM sntc_table);"
#         result = db.session.execute(queryString)
#
#         print(result, file=sys.stderr)
#
#         for row in result:
#             pn_code = row[0]
#             sntc = SNTC_TABLE()
#
#             sntc.pn_code = pn_code
#
#             if (
#                 SNTC_TABLE.query.with_entities(SNTC_TABLE.sntc_id)
#                 .filter_by(pn_code=pn_code)
#                 .first()
#                 is None
#             ):
#                 print("Inserted " + pn_code, file=sys.stderr)
#                 sntc.creation_date = datetime.now()
#                 sntc.modification_date = datetime.now()
#                 InsertDBData(sntc)
#             else:
#                 print("Updated " + pn_code, file=sys.stderr)
#                 sntc.modification_date = datetime.now()
#                 UpdateDBData(sntc)
#         return ("SUCCESS"), 200
#
#     except Exception:
#         traceback.print_exc()
#         return "Exception Occurred While SNTC Sync Inventory", 500
#
#
# @app.route("/syncToInventory", methods=["GET"])
# @token_required
# def SyncToInventory(user_data):
#     try:
#         results = SNTC_TABLE.query.all()
#
#         for sntc in results:
#
#             # UAM Device Sync
#             try:
#                 uam_rows = UAM_Device_Table.query.filter(
#                     UAM_Device_Table.pn_code == sntc.pn_code
#                 ).all()
#
#                 for uam in uam_rows:
#                     try:
#                         if sntc.hw_eos_date is not None:
#                             uam.hw_eos_date = sntc.hw_eos_date
#
#                         if sntc.hw_eol_date is not None:
#                             uam.hw_eol_date = sntc.hw_eol_date
#
#                         if sntc.sw_eos_date is not None:
#                             uam.sw_eos_date = sntc.sw_eos_date
#
#                         if sntc.sw_eol_date is not None:
#                             uam.sw_eol_date = sntc.sw_eol_date
#
#                         if sntc.manufacture_date is not None:
#                             uam.manufacture_date = sntc.manufacture_date
#
#                         UpdateDBData(uam)
#                     except Exception:
#                         traceback.print_exc()
#                         print(f"{uam.uam_id} - Error", file=sys.stderr)
#             except Exception:
#                 traceback.print_exc()
#
#
#
#             # Board Sync
#             try:
#                 board_rows = Board_Table.query.filter(
#                     Board_Table.pn_code == sntc.pn_code
#                 ).all()
#
#                 for board in board_rows:
#                     try:
#                         if sntc.hw_eos_date is not None:
#                             board.eos_date = sntc.hw_eos_date
#
#                         if sntc.hw_eol_date is not None:
#                             board.eol_date = sntc.hw_eol_date
#
#                         if sntc.manufacture_date is not None:
#                             board.manufacture_date = sntc.manufacture_date
#
#                         UpdateDBData(board)
#                     except Exception:
#                         traceback.print_exc()
#                         print(f"{board.board_id} - Error", file=sys.stderr)
#             except Exception:
#                 traceback.print_exc()
#
#
#
#             # Sub-Board Sync
#             try:
#                 subboard_rows = Subboard_Table.query.filter(
#                     Subboard_Table.pn_code == sntc.pn_code
#                 ).all()
#
#                 for subboard in subboard_rows:
#                     try:
#                         if sntc.hw_eos_date is not None:
#                             subboard.eos_date = sntc.hw_eos_date
#
#                         if sntc.hw_eol_date is not None:
#                             subboard.eol_date = sntc.hw_eol_date
#
#                         if sntc.manufacture_date is not None:
#                             subboard.manufacture_date = sntc.manufacture_date
#
#                         UpdateDBData(subboard)
#                     except Exception:
#                         traceback.print_exc()
#                         print(f"{subboard.subboard_id} - Error", file=sys.stderr)
#             except Exception:
#                 traceback.print_exc()
#
#             # SFP Sync
#             try:
#                 sfp_rows = Sfps_Table.query.filter(
#                     Sfps_Table.pn_code == sntc.pn_code
#                 ).all()
#
#                 for sfp in sfp_rows:
#                     try:
#                         if sntc.hw_eos_date is not None:
#                             sfp.eos_date = sntc.hw_eos_date
#
#                         if sntc.hw_eol_date is not None:
#                             sfp.eol_date = sntc.hw_eol_date
#
#                         UpdateDBData(sfp)
#                     except Exception:
#                         traceback.print_exc()
#                         print(f"{sfp.sfp_id} - Error", file=sys.stderr)
#             except Exception:
#                 traceback.print_exc()
#
#         return jsonify("Successfully Sync To Inventory"), 200
#
#     except Exception as e:
#         print(f"SNTC error occured {e}", file=sys.stderr)
#         return "Exception While Sync To Inventory", 500
#
#
# @app.route("/editSntc", methods=["POST"])
# @token_required
# def EditSntc(user_data):
#     try:
#         sntcObj = request.get_json()
#         print(sntcObj, file=sys.stderr)
#
#         sntc = SNTC_TABLE()
#         sntc.sntc_id = sntcObj["sntc_id"]
#         sntc.pn_code = sntcObj["pn_code"]
#         sntc.hw_eos_date = FormatStringDate(sntcObj["hw_eos_date"])
#         sntc.hw_eol_date = FormatStringDate(sntcObj["hw_eol_date"])
#         sntc.sw_eos_date = FormatStringDate(sntcObj["sw_eos_date"])
#         sntc.sw_eol_date = FormatStringDate(sntcObj["sw_eol_date"])
#         sntc.manufacture_date = FormatStringDate(sntcObj["manufacturer_date"])
#
#         print("Updated " + sntcObj["pn_code"], file=sys.stderr)
#         sntc.modification_date = datetime.now()
#         UpdateDBData(sntc)
#
#         return jsonify({"response": "success", "code": "200"})
#
#     except Exception:
#         traceback.print_exc()
#         return "Exception Occurred While SNTC Sync Inventory", 500
#
#
# @app.route("/addSNTC", methods=["POST"])
# @token_required
# def AddSntc(user_data):
#     # request.headers.get('X-Auth-Key') == session.get('token', None):
#     if True:
#         postData = request.get_json()
#
#         # print(postData,file=sys.stderr)
#         try:
#             for sntcObj in postData:
#                 sntc = SNTC_TABLE()
#
#                 print(sntcObj, file=sys.stderr)
#                 sntc.pn_code = sntcObj["pn_code"]
#
#                 if "hw_eos_date" in sntcObj:
#                     if sntcObj["hw_eos_date"] != "NA":
#                         try:
#                             print(sntcObj["hw_eos_date"], file=sys.stderr)
#                             sntc.hw_eos_date = datetime.strptime(
#                                 (sntcObj["hw_eos_date"]), "%d-%m-%Y"
#                             )
#                         except:
#                             print(
#                                 "Incorrect formatting in hw_eos_date", file=sys.stderr
#                             )
#                             traceback.print_exc()
#                 if "hw_eol_date" in sntcObj:
#                     if sntcObj["hw_eol_date"] != "NA":
#                         try:
#                             sntc.hw_eol_date = datetime.strptime(
#                                 (sntcObj["hw_eol_date"]), "%d-%m-%Y"
#                             )
#                         except:
#                             print(
#                                 "Incorrect formatting in hw_eol_date", file=sys.stderr
#                             )
#                 if "sw_eos_date" in sntcObj:
#                     if sntcObj["sw_eos_date"] != "NA":
#                         try:
#                             sntc.sw_eos_date = datetime.strptime(
#                                 (sntcObj["sw_eos_date"]), "%d-%m-%Y"
#                             )
#                         except:
#                             print(
#                                 "Incorrect formatting in sw_eos_date", file=sys.stderr
#                             )
#                 if "sw_eol_date" in sntcObj:
#                     if sntcObj["sw_eol_date"] != "NA":
#                         try:
#                             sntc.sw_eol_date = datetime.strptime(
#                                 (sntcObj["sw_eol_date"]), "%d-%m-%Y"
#                             )
#                         except:
#                             print(
#                                 "Incorrect formatting in sw_eol_date", file=sys.stderr
#                             )
#                 if "manufacturer_date" in sntcObj:
#                     if sntcObj["manufacturer_date"] != "NA":
#                         try:
#                             sntc.manufacture_date = datetime.strptime(
#                                 (sntcObj["manufacturer_date"]), "%d-%m-%Y"
#                             )
#                             # print(sntc.manufacture_date, file=sys.stderr)
#                         except:
#                             print(
#                                 "Incorrect formatting in manufactuer_date",
#                                 file=sys.stderr,
#                             )
#                 # if 'item_desc' in sntcObj:
#                 #      if sntcObj['item_desc'] != 'NA':
#                 #         try:
#                 #             sntc.item_desc =sntcObj['item_desc']
#                 #             #print(sntc.manufacture_date, file=sys.stderr)
#                 #         except:
#                 #             print("Incorrect Value in item description", file=sys.stderr)
#                 # if 'item_code' in sntcObj:
#                 #      if sntcObj['item_code'] != 'NA':
#                 #         try:
#                 #             sntc.item_code =sntcObj['item_code']
#                 #             #print(sntc.manufacture_date, file=sys.stderr)
#                 #         except:
#                 #             print("Incorrect Value in item description", file=sys.stderr)
#
#                 if (
#                     SNTC_TABLE.query.with_entities(SNTC_TABLE.sntc_id)
#                     .filter_by(pn_code=sntcObj["pn_code"])
#                     .first()
#                     is not None
#                 ):
#                     sntc.sntc_id = (
#                         SNTC_TABLE.query.with_entities(SNTC_TABLE.sntc_id)
#                         .filter_by(pn_code=sntcObj["pn_code"])
#                         .first()[0]
#                     )
#                     print("Updated " + sntcObj["pn_code"], file=sys.stderr)
#                     sntc.modification_date = datetime.now()
#                     UpdateData(sntc)
#                 else:
#                     print("Inserted " + sntcObj["pn_code"], file=sys.stderr)
#                     sntc.creation_date = datetime.now()
#                     sntc.modification_date = datetime.now()
#                     InsertData(sntc)
#
#             return "Data Added/Updated Successfully", 200
#         except Exception as e:
#             traceback.print_exc()
#             return "Failed To Update Data", 500
#     else:
#         print("Authentication Failed", file=sys.stderr)
#         return jsonify({"message": "Authentication Failed"}), 401
#
#
# @app.route("/deletePnCode", methods=["POST"])
# @token_required
# def DeletePnCode(user_data):
#     if True:  # session.get('token', None):
#         posObj = request.get_json()
#         print(posObj, file=sys.stderr)
#         print(f"PnCode Data received is:  {posObj}", file=sys.stderr)
#
#         for obj in posObj.get("user_ids"):
#             posID = SNTC_TABLE.query.filter(SNTC_TABLE.pn_code == obj).first()
#             print(posID, file=sys.stderr)
#             if obj:
#                 db.session.delete(posID)
#                 db.session.commit()
#         return jsonify({"response": "success", "code": "200"})
#     else:
#         print("Authentication Failed", file=sys.stderr)
#         return jsonify({"message": "Authentication Failed"}), 401
