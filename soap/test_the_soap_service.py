import pytest
from models import Base, engine
from service import ProductService


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield


def test_create_and_get_product():
    product_id = ProductService.CreateProduct(None, "TestItem", 5, 10.99)
    assert isinstance(product_id, int) and product_id > 0

    result = ProductService.GetProduct(None, product_id)
    assert "TestItem" in result
    assert "Qty: 5" in result


def test_update_product():
    product_id = ProductService.CreateProduct(None, "ToUpdate", 1, 1.0)
    success = ProductService.UpdateProduct(None, product_id, "Updated", 10, 20.0)
    assert success

    result = ProductService.GetProduct(None, product_id)
    assert "Updated" in result
    assert "Qty: 10" in result


def test_delete_product():
    product_id = ProductService.CreateProduct(None, "ToDelete", 1, 1.0)
    success = ProductService.DeleteProduct(None, product_id)
    assert success

    result = ProductService.GetProduct(None, product_id)
    assert result == "Product not found"


def test_invalid_quantity():
    with pytest.raises(ValueError):
        ProductService.CreateProduct(None, "Bad", -1, 10.0)
