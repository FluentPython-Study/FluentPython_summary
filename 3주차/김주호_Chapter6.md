# Chap 6. 일급 함수 디자인 패턴

먼저, 전략 패턴에 대해 일급 함수를 이용해서 단순화할 수 있는 대안을 살펴본다. 전략 패턴을 리팩토링하고 명령 패턴에 대해 설명하면서 어느 정도 식견을 넓힌다.

## 6.1 사례: 전략 패턴의 리팩토링
### 6.1.1 고전적인 전략

- 전략 패턴 : 일련의 알고리즘을 정의하고 각각을 하나의 클래스 안에 넣어서 교체하기 쉽게 만든다. 전략을 이요하면 사용하는 클라이언트에 따라 알고리즘을 독립적으로 변경할 수 있다.


```python
from abc import ABC, abstractmethod
from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')


class LineItem:

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order:  # the Context

    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


class Promotion(ABC):  # the Strategy: an Abstract Base Class

    @abstractmethod
    def discount(self, order):
        """Return discount as a positive dollar amount"""


class FidelityPromo(Promotion):  # first Concrete Strategy
    """5% discount for customers with 1000 or more fidelity points"""

    def discount(self, order):
        return order.total() * .05 if order.customer.fidelity >= 1000 else 0


class BulkItemPromo(Promotion):  # second Concrete Strategy
    """10% discount for each LineItem with 20 or more units"""

    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * .1
        return discount


class LargeOrderPromo(Promotion):  # third Concrete Strategy
    """7% discount for orders with 10 or more distinct items"""

    def discount(self, order):
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * .07
        return 0
```


```python
## 외부에서 사용

joe = Customer('John Doe', 0)
ann = Customer('Ann Smith', 1100)
cart = [LineItem('banana', 4, .5),
LineItem('apple', 10, 1.5),
LineItem('watermellon', 5, 5.0)]
Order(joe, cart, FidelityPromo())

Order(ann, cart, FidelityPromo())

banana_cart = [LineItem('banana', 30, .5),
LineItem('apple', 10, 1.5)]
Order(joe, banana_cart, BulkItemPromo())

long_order = [LineItem(str(item_code), 1, 1.0)
for item_code in range(10)]
Order(joe, long_order, LargeOrderPromo())

print(Order(joe, cart, LargeOrderPromo()))

```

    <Order total: 42.00 due: 42.00>



### 6.1.2 함수 지향 전략

```python
from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')


class LineItem:

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order:  # the Context

    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)  # <1>
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())

# <2>

def fidelity_promo(order):  # <3>
    """5% discount for customers with 1000 or more fidelity points"""
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0


def bulk_item_promo(order):
    """10% discount for each LineItem with 20 or more units"""
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount


def large_order_promo(order):
    """7% discount for orders with 10 or more distinct items"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0
```


```python
## 외부에서 사용 : 함수를 인자로 집어넣는다.

joe = Customer('John Doe', 0)
ann = Customer('Ann Smith', 1100)
cart = [LineItem('banana', 4, .5),
LineItem('apple', 10, 1.5),

LineItem('watermellon', 5, 5.0)]
Order(joe, cart, fidelity_promo)

Order(ann, cart, fidelity_promo)

banana_cart = [LineItem('banana', 30, .5),
LineItem('apple', 10, 1.5)]
Order(joe, banana_cart, bulk_item_promo)

long_order = [LineItem(str(item_code), 1, 1.0)
for item_code in range(10)]
Order(joe, long_order, large_order_promo)

print(Order(joe, cart, large_order_promo))
```

    <Order total: 42.00 due: 42.00>



## 6.2 명령

입력이 들어올 때, 하나의 메소드에서 입력에 연결된 메소드를 호출해서 처리하는 것이 아니라, 각 기능을 명령 클래스로 감싸서 
- 입력을 처리하는 로직과, 
- 명령을 분배하는 로직
- 명령을 실행하는 로직
을 분리한다. 각 실행 로직을 담당하는 클래스에 상태를 저장한다면, 실행 취소(undo) 기능도 dependency 없이 구현할 수 있게 된다.