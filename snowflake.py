class Snowflake:
    def __init__(self, snowflake: int):
        self.snowflake = snowflake
        self.timestamp = (snowflake >> 22) + 1420070400000
        self.wid = (snowflake & 0x3E0000) >> 17
        self.pid = (snowflake & 0x1F000) >> 12
        self.increment = snowflake & 0xFFF
    def __int__(self):
        return self.snowflake
    def __str__(self):
        return str(int(self))
    def payload(self):
        return int(self)
    def from_timestamp(timestamp_ms:int):
        return Snowflake((timestamp_ms - DISCORD_EPOCH) << 22)
