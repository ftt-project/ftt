import pytest

from ftt.brokers.brokerage_service import BrokerageService


class TestBrokerageService:
    @pytest.fixture
    def subject(self):
        return BrokerageService

    @pytest.fixture
    def x_brokerage_service(self, mocker):
        return mocker.MagicMock()

    def test_provider_name(self, subject, x_brokerage_service):
        x_brokerage_service.provider_name = "X"
        service = subject(x_brokerage_service)
        assert service.provider_name == "X"

    def test_open_positions(self, subject, x_brokerage_service):
        service = subject(x_brokerage_service)
        service.open_positions()
        x_brokerage_service.obtain_open_positions.assert_called_once()

    def test_obtain_server_time(self, subject, x_brokerage_service):
        service = subject(x_brokerage_service)
        service.obtain_server_time()
        x_brokerage_service.obtain_server_time.assert_called_once()

    @pytest.mark.skip(reason="Not implemented")
    def test_place_order(self, subject):
        pass
