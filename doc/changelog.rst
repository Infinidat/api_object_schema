Changelog
=========

* :feature:`2` Support a way to forbid field names/api_names overrides
* :feature:`-` Support documentation (currently only changelog)
* :feature:`-` Add python3.6 & remove python 2.6, 3.3 & 3.4 from travis
* :release:`1.5.1 <02-02-2015>`
* :feature:`-` ConstBinding should return the const from api object
* :feature:`-` Remove support for bound fields
* :release:`1.5.0 <19-10-2014>`
* :feature:`-` Make obj.fields produce bound fields (fields that are aware of the object they're attached to)
* :release:`1.4.3 <10-07-2014>`
* :bug:`- major` Fix field binding coercion
* :release:`1.4.2 <03-07-2014>`
* :feature:`-` Allow typeinfo types to be strings, lazily loading the actual types they refer to
* :release:`1.4.1 <30-06-2014>`
* :bug:`- major` Fix Python 3 support
* :release:`1.4.0 <30-06-2014>`
* :feature:`-` Refactor schema
* :feature:`-` Add ``api_object_schema.utils.loose_isinstance``
* :feature:`-` Refactor field bindings
* :release:`1.3.3 <09-04-2014>`
* :bug:`- major` Fix ``Field.externalize`` of None value
* :release:`1.3.2 <03-04-2014>`
* :feature:`-` CountBinding can handle both list's name & list's getter function
* :feature:`-` Improve unittests
* :release:`1.3.1 <24-03-2014>`
* :feature:`-` Allow both integers and longs under Python 2.x
* :release:`1.3.0 <20-03-2014>`
* :feature:`-` Improve unittests
* :release:`1.2.9 <19-03-2014>`
* :feature:`-` Don't accept booleans as integers when internalizing fields
* :release:`1.2.8 <19-03-2014>`
* :feature:`-` Better validation of api_types
* :release:`1.2.7 <13-03-2014>`
* :feature:`-` Added ``Field.get_is_visible``
* :release:`1.2.6 <10-03-2014>`
* :feature:`-` Allow None values when internalizing values
* :release:`1.2.5 <09-03-2014>`
* :feature:`-` Added Field externalize & internalize methods
* :release:`1.2.4 <26-02-2014>`
* :feature:`-` Added ``Field.sorting_key``
* :release:`1.2.3 <18-02-2014>`
* :feature:`-` Added ``Field.notify_added_to_class``
* :release:`1.2.2 <18-02-2014>`
* :feature:`-` Added ``Fields.get_by_api_name``
* :release:`1.2.1 <18-02-2014>`
* :feature:`-` Added ``Field.is_sortable``
* :release:`1.2.0 <18-02-2014>`
* :feature:`-` Add additional bindings
* :release:`1.1.0 <17-02-2014>`
* :feature:`-` Support field bindings
* :release:`1.0.0 <09-02-2014>`
