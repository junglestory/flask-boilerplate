from flask import Flask, jsonify
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
            ORDER BY SEQ ASC 
        '''        

        list = db.select_query_as_dicts(query)

        return jsonify(list)


if __name__ == "__main__":    
    app.run(debug=True, host='0.0.0.0', port=5000)

