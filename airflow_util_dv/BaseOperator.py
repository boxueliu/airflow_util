from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.oracle_hook import OracleHook


class NewBaseOperator(BaseOperator):
    template_fields = ('sql',)
    template_ext = ('.sql',)
    ui_color = '#ededed'

    @apply_defaults
    def __init__(
            self, file, oracle_conn_id='oracle_default', parameters=None,
            autocommit=False, *args, **kwargs):
        super(NewBaseOperator, self).__init__(*args, **kwargs)
        self.oracle_conn_id = oracle_conn_id
        self.sql_file = file
        self.sql = ''
        self.autocommit = autocommit
        self.parameters = parameters

    def execute(self, context):
        self.sql = ''
        self.log.info('Executing: %s', self.sql)
        hook = OracleHook(oracle_conn_id=self.oracle_conn_id)
        hook.run(
            self.sql,
            autocommit=self.autocommit,
            parameters=self.parameters)