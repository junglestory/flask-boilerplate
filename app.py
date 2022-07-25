from flask import Flask, jsonify, request
import common.logger as logger
from common.db_manager import DatabaseManager

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

PROJECT_NAME = "flask"
DATASOURCE_ID = "local"

# Create logger
logger = logger.create_logger(PROJECT_NAME)

db = DatabaseManager(DATASOURCE_ID)
db.connection()

@app.route('/news', defaults={'site_id': ''}, methods=['GET'])
@app.route('/news/<site_id>', methods=['GET'])
def news(site_id):
        query = '''
            SELECT SEQ, JOURNAL_ID, TITLE, PUBLISH_DATE, WRITER, CONTENT, REG_DATE 
            FROM news 
            {}
            ORDER BY SEQ ASC 
        '''        

        where  = "";

        if site_id != "":
            where = "WHERE JOURNAL_ID = '{}'".format(site_id)
        
        list = db.select_query_as_dicts(query.format(where))

        return jsonify(list)


@app.route('/news', methods=['POST'])
def news_insert():
        param = request.form

        if param != None:
            query = '''
                INSERT INTO news (TITLE, LINK_URL, WRITER, PUBLISH_DATE, CONTENT, JOURNAL_ID, REG_DATE)
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    now()
                )                    
            '''        
            
            data = (param['title'], param['link_url'], param['writer'], param['publish_date'], param['content'], param['journal_id'])            
            result = db.execute_query(query, data)
            
            result_code = "0000"
            result_message = "Success"
            status_code = 200

            if result != 0:            
                result_code = "9999"
                result_message = "Failed"
                status_code = 400

        result_data = {"data": "", "resultCode": "{}".format(result_code), "resultMessage": "{}".format(result_message), "statusCode": status_code}
        
        return jsonify(result_data)



@app.route('/news/<site_id>', methods=['DELETE'])
def news_delete(site_id):
        query = '''
            DELETE 
            FROM news 
            WHERE SEQ = {}
        '''        
        
        list = db.select_query_as_dicts(query.format(site_id))

        return jsonify(list)


@app.route('/news', methods=['PUT'])
def news_update():
        query = '''
            DELETE 
            FROM news 
            WHERE SEQ = {}
        '''        
        
        # list = db.select_query_as_dicts(query.format(site_id))

        return jsonify({"hello":"world!"})



if __name__ == "__main__":    
    app.run(debug=True, host='0.0.0.0', port=5000)

