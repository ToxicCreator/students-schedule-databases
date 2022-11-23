from neo4j import GraphDatabase


class Neo4jManager():
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(Neo4jManager, self).__new__(self)
        return self.instance


    def __init__(self):
        self.database = GraphDatabase.driver(
            uri="bolt://localhost:7687",
            auth=('neo4j', 'admin')
        )
        self.session = self.database.session()
        # try:
        #     database.session().run("Match () return 1 Limit 1")
        #     return database
        # except:
        #     print("\nFailed to connect to Neo4J")
        #     sys.exit()


    def create_node(self, label, parameters):
        query = f'''
            CREATE (node:{label})
            SET node = $params
            RETURN node;
        '''
        return self.execute(query, parameters).single()[0]


    def create_merge(self, from_, to, label=''):
        query = f'''
            MATCH (from) WITH from
            MATCH (to)
                WHERE ID(from) = {from_.element_id} 
                AND ID(to) = {to.element_id}
            CREATE (from)-[rel:{label}]->(to) 
            RETURN from, to, rel;
        '''
        return self.execute(query).single()


    def read_all(self):
        query = 'MATCH (n) RETURN n;'
        return self.execute(query).values()


    def clear_all(self):
        self.clear_with_relationships()
        self.clear_single()
        print('Remove all!')


    def clear_single(self):
        query = 'MATCH (n) DELETE n;'
        self.execute(query)
        print('Remove single node.')


    def clear_with_relationships(self):
        query = 'MATCH (n)-[r]-() DELETE n, r;'
        self.execute(query)
        print('Remove nodes with relationships.')


    def execute(self, query, params={}):
        return self.session.run(query, params=params)