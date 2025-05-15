from odoo import api, models, fields

class XAttrMixin(models.AbstractModel):
    _name = "x.attr.mixin"
    
    # find_or_create :: focr
    def find_or_create(self, search_criteria, creation_values=None):
        """
        Finds the first record matching the search criteria or creates a new one,
        handling search_criteria and creation_values flexibly.

        Args:
            search_criteria (list or dict):
                - A domain list for searching existing records.
                - OR a dictionary of field values to search for (and use for creation
                  if no record is found).  If a dict, it's converted to a domain.
            creation_values (dict, optional):
                - A dictionary of field values to use when creating a new record
                  if none is found.
                - If None, the search_criteria is used as the creation values
                  (after converting it to a dict if it was a domain list).
                - This argument takes precedence over any values derived from
                  search_criteria.

        Returns:
            recordset: The existing record (if found) or the newly created record.
        
        example:
        m.find_or_create({'name': 'person'})
        """
        # Convert search_criteria to a domain list if it's a dict
        if isinstance(search_criteria, dict):
            domain = [(field, '=', value) for field, value in search_criteria.items()]
        else:
            domain = search_criteria  # Assume it's already a domain list

        existing_record = self.search(domain, limit=1)
        if existing_record:
            return existing_record
        if creation_values is None:
            # Use search_criteria as creation values
            if isinstance(search_criteria, dict):
                vals_to_create = search_criteria.copy()  # Use a copy to avoid modifying original
            else:
                vals_to_create = {}
                for field, operator, value in search_criteria:
                    if operator == '=':
                        vals_to_create[field] = value
        else:
            # creation_values is provided, use it
            vals_to_create = creation_values.copy() # Use a copy

        return self.create(vals_to_create)

    def find_or_create_with_defaults(self, search_criteria, defaults=None):
        """
        Finds the first record matching the search criteria or creates a new one
        using the merged search criteria and provided defaults.

        Args:
            search_criteria (list): A domain list for searching existing records.
            defaults (dict, optional): A dictionary of default field values to use
                                        during creation if no record is found.
                                        Defaults to None.

        Returns:
            recordset: The existing record (if found) or the newly created record.
        """
        existing_record = self.search(search_criteria, limit=1)
        if existing_record:
            return existing_record
        else:
            vals_to_create = {}
            # Add search criteria as creation values
            for field, operator, value in search_criteria:
                if operator == '=' and field not in vals_to_create:
                    vals_to_create[field] = value
            # Merge with defaults, prioritizing defaults if there's a conflict
            if defaults:
                vals_to_create.update(defaults)
            return self.create(vals_to_create)
    """
    def example_usage(self):
        # Example 1: Find by name, create with name and default value
        record1 = self.find_or_create([('name', '=', 'Existing Name')])
        print(f"Record 1: {record1}")

        record2 = self.find_or_create([('name', '=', 'New Name')], {'value': 10})
        print(f"Record 2: {record2}")

        # Example 2: Find by name, create with merged search criteria and defaults
        record3 = self.find_or_create_with_defaults([('name', '=', 'Another Existing')], {'active': False})
        print(f"Record 3: {record3}")

        record4 = self.find_or_create_with_defaults([('name', '=', 'Brand New')], {'value': 25, 'active': True})
        print(f"Record 4: {record4}")
    """

class XAttr(models.Model):
    _name = 'x.attr'
    _inherit = ["x.attr.mixin"]

# thx gemini
class XModel(models.Model):
    _name = 'base_om.x_model'
    _description = 'x model'
    _inherit = 'x.attr'
    # pass

class XTransientModel(models.TransientModel, XAttr):
    _name = 'base_om.x_model'
    _description = 'x model'
    # pass
