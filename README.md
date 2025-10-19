# Issues with Monolothic Approach
1. Tight Coupling: All  app logic (Database operations, validation, and console output) is in one file, making changes risky and testing difficult.
2. Limited Reusability: Components cannot be reused in other contexts (for example: Modular imports, web API).
3. Concurrency & Deployment Issues: Hard to scale horizontally; entire script must be redeployed for each minor changes.


# SOAP 
To test it run this, instead of a UI:
```
pytest soap/test_the_soap_service.py 
```

## Here is the OUTPUT
```
 ===============test session starts ==============================================================================================
            platform linux -- Python 3.10.19, pytest-8.4.2, pluggy-1.6.0
            rootdir: /home/wael/Code/TPs_AOS/TP1
            configfile: pyproject.toml
            plugins: anyio-4.11.0
            collected 4 items
                                                                                                                                                                                                                            ------------
            soap/test_the_soap_service.py ....                                                                                                                                                                       [100%]

=================4 passed in 0.22s ===============================================================================================
```

## SOAP vs MONOLITHIC
Thanks to WSDL, we can enforce structure and we can clearly see this in this snippet of XML/WSDL file:
```
<xs:complexType name="CreateProduct">
  <xs:sequence>
    <xs:element name="name" type="xs:string" minOccurs="0"/>
    <xs:element name="quantity" type="xs:integer" minOccurs="0" nillable="true"/>
    <xs:element name="price" type="xs:float" minOccurs="0" nillable="true"/>
  </xs:sequence>
</xs:complexType>
```
We can see the type checks and for example name is string not nullable.
ALso we can see that is more modular than our monolithic approach, so we can import and do small changes without redeploying the whole application.
