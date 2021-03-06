import pytest

from lms.services import CanvasAPIError
from lms.views.api.canvas.files import FilesAPIViews


class TestListFiles:
    def test_it_gets_the_list_of_files_from_canvas(
        self, canvas_api_client, pyramid_request
    ):
        FilesAPIViews(pyramid_request).list_files()

        canvas_api_client.list_files.assert_called_once_with("test_course_id")

    def test_it_returns_the_list_of_files(self, canvas_api_client, pyramid_request):
        assert (
            FilesAPIViews(pyramid_request).list_files()
            == canvas_api_client.list_files.return_value
        )

    # CanvasAPIError's are caught and handled by an exception view, so the
    # normal view just lets them raise.
    def test_it_doesnt_catch_CanvasAPIErrors_from_list_files(
        self, canvas_api_client, pyramid_request
    ):
        canvas_api_client.list_files.side_effect = CanvasAPIError("Oops")

        with pytest.raises(CanvasAPIError, match="Oops"):
            FilesAPIViews(pyramid_request).list_files()

    @pytest.fixture
    def pyramid_request(self, pyramid_request):
        pyramid_request.matchdict = {"course_id": "test_course_id"}
        return pyramid_request


class TestViaURL:
    def test_it_gets_the_public_url_from_canvas(
        self, canvas_api_client, pyramid_request
    ):
        FilesAPIViews(pyramid_request).via_url()

        canvas_api_client.public_url.assert_called_once_with("test_file_id")

    def test_it_gets_the_via_url_for_the_public_url(
        self, canvas_api_client, pyramid_request, helpers
    ):
        FilesAPIViews(pyramid_request).via_url()

        helpers.via_url.assert_called_once_with(
            pyramid_request,
            canvas_api_client.public_url.return_value,
            content_type="pdf",
        )

    # CanvasAPIError's are caught and handled by an exception view, so the
    # normal view just lets them raise.
    def test_doesnt_catch_CanvasAPIErrors_from_public_url(
        self, canvas_api_client, pyramid_request
    ):
        canvas_api_client.public_url.side_effect = CanvasAPIError("Oops")

        with pytest.raises(CanvasAPIError, match="Oops"):
            FilesAPIViews(pyramid_request).via_url()

    def test_it_returns_the_via_url(self, pyramid_request, helpers):
        data = FilesAPIViews(pyramid_request).via_url()

        assert data["via_url"] == helpers.via_url.return_value

    @pytest.fixture
    def pyramid_request(self, pyramid_request):
        pyramid_request.matchdict = {"file_id": "test_file_id"}
        return pyramid_request


@pytest.fixture(autouse=True)
def helpers(patch):
    return patch("lms.views.api.canvas.files.helpers")


pytestmark = pytest.mark.usefixtures("canvas_api_client")
