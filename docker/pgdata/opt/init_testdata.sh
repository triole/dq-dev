#!/bin/bash

fol="${HOME}/source/testing/sql/postgres/"
role="daiquiri_data"

psql -U ${role} daiquiri_data <"${fol}/data.sql"
psql -U ${role} daiquiri_data <"${fol}/test.sql"
psql -U ${role} test_daiquiri_data <"${fol}/data.sql"
psql -U ${role} test_daiquiri_data <"${fol}/test.sql"
