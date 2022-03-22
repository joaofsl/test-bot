#!/usr/bin/python
# -*- coding: utf-8 -*-

import base
import json
import appier

HS_CODE = "640411"
""" Harmonized System (HS) code, an internationally standardized system
of names and numbers to classify traded products."""

class Logic(base.Logic):

    def groups(self, ctx):
        return ["main"]

    def minimum_initials(self, group, ctx):
        return 2

    def maximum_initials(self, group, ctx):
        return 8

    def supported_characters(self, group, index, ctx):
        return "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@-. "

    def build_shopify_product(
        self,
        product_title,
        original_product,
        parts,
        variant = None,
        version = None,
        initials_extra = None,
        size = None,
        scale = None,
        gender = None,
        size_scaled = None,
        currency = None,
        country = None,
        flag = None,
    ):
        """
        Generates a product payload (dictionary) ready to be used for the
        creation of an equivalent Shopify product.

        The structure of the payload must respect the equivalent structure
        of the product under the Shopify API.

        :type product_title: String
        :param product_title: The title that is going to be used for the
        Shopify product.
        :rtype: Dictionary
        :return: A dictionary containing the payload for the model, which includes
        the parsed SKU, EAN and HS code.
        """

        title = product_title if product_title else original_product["title"]

        base_url = appier.conf("RIPE_CORE_URL", "https://ripe-core-sbx.platforme.com")

        # determines the scaled size either by using the given one or
        # using RIPE API to calculate it if size, scale and gender are given
        if not size_scaled and size and scale and gender:
            params = dict(
                scale = scale,
                value = size,
                gender = gender
            )
            size_url = "%s/api/sizes/native_to_size" % base_url
            size_scaled = self.http.get(size_url, params)["value"]

        params = dict(
            brand = "cariuma",
            model = "oca_low",
            variant = variant,
            version = version,
            p = parts,
            initials_extra = initials_extra,
            currency = currency,
            country = country,
            flag = flag,
            size = size,
            gender = gender
        )
        price_url = "%s/api/config/price" % base_url
        price = self.http.get(price_url, params)
        price_final = price["total"]["price_final"]

        # tries to get the SKU for this configuration failing gracefully
        # in case none is found (with expected error code 400)
        sku_url = "%s/api/config/sku" % base_url
        sku_config = self.http.get(sku_url, params)

        sku_ean = sku_config["sku"]
        sku, ean, _gender = sku_ean.split(".", 2)

        customized_variant = dict(price = price_final)
        customized_variant["sku"] = sku
        customized_variant["barcode"] = ean
        customized_variant["inventory_item"] = dict(
            harmonized_system_code = HS_CODE,
            sku = sku
        )

        # creates the sequence that is going to hold the options
        # (dimensions) and the variant that may have multiple options
        options = []

        # determines if the scaled size is a decimal one, this is going
        # to be used to use the integer or the decimal version of the
        # size scaling, avoding unnecessary decimal representation of the
        # value in the UI (UX optimization process)
        is_decimal = not size_scaled % 1 == 0

        # adds size dimension and value to the sequence of option values,
        # notice the integer conversion, if needed
        options.append(dict(name = "Size"))
        customized_variant["option1"] = size_scaled if is_decimal else int(size_scaled)

        # add scale dimension and value to the sequence of option values
        # explicitly stating the scale associated
        options.append(dict(name = "Scale"))
        customized_variant["option2"] = scale.upper()

        # adds gender dimension and value to the sequence of option values
        options.append(dict(name = "Gender"))
        customized_variant["option3"] = gender.capitalize()

        return dict(
            title = title,
            options = options,
            variants = [customized_variant],
            metafields = [
                dict(
                    namespace = "seo",
                    key = "hidden",
                    value = 1,
                    value_type = "integer"
                ),
                dict(
                    namespace = "platforme",
                    key = "context",
                    value = json.dumps(dict(
                        brand = "cariuma",
                        model = "oca_low",
                        variant = variant,
                        version = version,
                        parts = parts,
                        initials_extra = initials_extra,
                        size = size,
                        scale = scale,
                        gender = gender,
                        size_scaled = size_scaled,
                        currency = currency,
                        country = country,
                        flag = flag
                    )),
                    value_type = "json_string"
                )
            ],
            product_type = "Platforme",
            tags = "platforme"
        )
