# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
#  Copyright by KNIME AG, Zurich, Switzerland
#  Website: http://www.knime.com; Email: contact@knime.com
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License, Version 3, as
#  published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses>.
#
#  Additional permission under GNU GPL version 3 section 7:
#
#  KNIME interoperates with ECLIPSE solely via ECLIPSE's plug-in APIs.
#  Hence, KNIME and ECLIPSE are both independent programs and are not
#  derived from each other. Should, however, the interpretation of the
#  GNU GPL Version 3 ("License") under any applicable laws result in
#  KNIME and ECLIPSE being a combined program, KNIME AG herewith grants
#  you the additional permission to use and propagate KNIME together with
#  ECLIPSE with only the license terms in place for ECLIPSE applying to
#  ECLIPSE and the GNU GPL Version 3 applying for KNIME, provided the
#  license terms of ECLIPSE themselves allow for the respective use and
#  propagation of ECLIPSE together with KNIME.
#
#  Additional permission relating to nodes for KNIME that extend the Node
#  Extension (and in particular that are based on subclasses of NodeModel,
#  NodeDialog, and NodeView) and that only interoperate with KNIME through
#  standard APIs ("Nodes"):
#  Nodes are deemed to be separate and independent programs and to not be
#  covered works.  Notwithstanding anything to the contrary in the
#  License, the License does not apply to Nodes, you are not required to
#  license Nodes under the License, and you are granted a license to
#  prepare and propagate Nodes, in each case even if such Nodes are
#  propagated with or for interoperation with KNIME.  The owner of a Node
#  may freely choose the license terms applicable to such Node, including
#  when such Node is propagated with or for interoperation with KNIME.
# ------------------------------------------------------------------------

"""
Defines a PythonValueFactory that determines how RDKit cells
are read and written from/to the underlying table in Python.

@author Carsten Haubold, KNIME GmbH, Konstanz, Germany
"""
import logging
import knime_types as kt

LOGGER = logging.getLogger(__name__)

try:
    # We cannot import rdkit at the top of the file because it would then be required
    # everywhere, even if we do not use the RDKit columns or don't even
    # have an RDKit column in the table but the type is registered.
    # All Python environments used in KNIME would then have to provide rdkit,
    # which we don't want.
    from rdkit import Chem
    from rdkit.Chem.rdChemReactions import ChemicalReaction

except ImportError as e:
    LOGGER.info(
        "RDKit type support not available because 'rdkit' could not be imported", e
    )

    # we define a dummy type Chem.Mol to be used instead.
    # Any attempt to work with this data will fail.
    class Chem:
        class Mol:
            pass

    class ChemicalReaction:
        pass


class RDKitMolAdapterValueFactory(kt.PythonValueFactory):
    def __init__(self):
        kt.PythonValueFactory.__init__(self, Chem.Mol)

    def decode(self, storage):
        if storage is None:
            return None

        value = Chem.Mol(storage["0"])
        return value

    def encode(self, value):
        if value is None:
            return None
        return {"0": value.ToBinary(), "1": None}

    def can_convert(self, value):
        return type(value) == Chem.Mol


class RDKitMolValueFactory(kt.PythonValueFactory):
    def __init__(self):
        kt.PythonValueFactory.__init__(self, Chem.Mol)

    def decode(self, storage):
        if storage is None:
            return None
        return Chem.Mol(storage)

    def encode(self, value):
        if value is None:
            return None
        return value.ToBinary()


class RDKitReactionValueFactory(kt.PythonValueFactory):
    def __init__(self):
        kt.PythonValueFactory.__init__(self, ChemicalReaction)

    def decode(self, storage):
        if storage is None:
            return None
        return ChemicalReaction(storage)

    def encode(self, value):
        if value is None:
            return None
        return value.ToBinary()
