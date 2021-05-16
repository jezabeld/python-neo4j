from neo import Singleton, NeoDB, exit_handler

def test_singleton():
    print("[Test Singleton] should return always the same instance.")

    class TestSingleton(Singleton):
        count=0
        
        def increment(self, num):
            self.count += num

    instance1 = TestSingleton()
    instance1.increment(10)

    instance2 = TestSingleton()
    instance2.increment(10)

    assert instance2.count == 20

def test_NeoDB_get_driver_creation(mocker):
    print("[Test NeoDB Get Driver] should return new driver instance.")

    driver_returned_instace = "driver_returned_instace"
    mocker.patch('neo4j.GraphDatabase.driver', return_value = driver_returned_instace)
    mocker.patch('atexit.register')
    mocker.patch('os.getenv', return_value='')

    neodb = NeoDB()
    assert  neodb.get_driver() == driver_returned_instace
    neodb.driver = None


def test_NeoDB_get_driver_cached(mocker):
    print("[Test NeoDB Get Driver] should return existing driver instance.")

    cached_driver = "cached_driver"
    driver_returned_instace = "driver_returned_instace"
    mocker.patch('neo4j.GraphDatabase.driver', return_value = driver_returned_instace)
    mocker.patch('atexit.register')
    mocker.patch('os.getenv', return_value='')

    neodb = NeoDB()
    neodb.driver = cached_driver
    
    assert  neodb.get_driver() == cached_driver
    neodb.driver = None


def test_NeoDB_get_driver_get_env(mocker):
    print("[Test NeoDB Get Driver] should pass env_vars to database.")

    def get_env_mock(x):
        my_dict = {'DATABASE_USERNAME': 'DATABASE_USERNAME',
                    'DATABASE_PASSWORD': 'DATABASE_PASSWORD',
                    'DATABASE_URL': 'DATABASE_URL'}
        return my_dict[x]
    
    def driver_mock(url, auth):
        return url + '-' + auth[0] + '-' + auth[1]

    mocker.patch('os.getenv', get_env_mock)
    mocker.patch('neo4j.GraphDatabase.driver', driver_mock)

    neodb = NeoDB()
    driver = neodb.get_driver()

    assert driver == 'DATABASE_URL-DATABASE_USERNAME-DATABASE_PASSWORD'
    neodb.driver = None

def test_NeoDB_get_session(mocker):
    print("[Test NeoDB Get Session] should return driver session")

    driver_session = 'driver_session'

    class DriverMock:
        def session(self):
            return driver_session

    neodb = NeoDB()
    neodb.driver = DriverMock()

    assert neodb.get_session() == driver_session
    neodb.driver = None

def test_NeoDB_close_driver(mocker):
    print("[Test NeoDB Get Session] should call only with cached driver")

    neodb = NeoDB()
    neodb.driver = mocker.Mock()
    neodb.close_driver()

    neodb.driver.close.assert_called_once()
    neodb.driver = None
    neodb.close_driver()

def test_exit_handler(mocker):
    print("[Test Exit Handler] should close driver")

    instance_mock = mocker.Mock()

    def mock_instance():
        return instance_mock

    mocker.patch('neo.NeoDB', mock_instance)
    exit_handler()
    instance_mock.close_driver.assert_called_once()