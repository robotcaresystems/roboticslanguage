#
#   This is the Robotics Language compiler
#
#   Parse.py: Parses the  language
#
#   Created on: 11 February, 2019
#       Author: Gabriel A. D. Lopes
#      Licence: Apache 2.0
#    Copyright: 2014-2017 Robot Care Systems BV, The Hague, The Netherlands. All rights reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import os
import yaml
import copy
from lxml import etree
from jinja2 import Template
from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Inputs.RoL import Parse as RoL
from RoboticsLanguage.Tools import DictionaryToXML


# def getType(value):
#   mapping = {'str': 'Strings', 'int': 'Integers', 'float': 'Reals', 'bool': 'Booleans'}
#
#   return mapping[filter(lambda x: type(value) is x, [bool, int, float, str])[0].__name__]
#
#
# def convertParameters(input):
#   output = copy.copy(input)
#
#   # extract parameters
#   output['parameters'] = []
#   for key, value in input['parameters'].iteritems():
#     type = getType(value)
#     if type == 'Strings':
#       value = '"' + value + '"'
#     output['parameters'].append({'name': key, 'type': getType(value), 'value': value})
#
#   # extract topics
#   output['topics'] = []
#   for key, value in input['topics'].iteritems():
#     [name, type] = value.split(' ')
#     output['topics'].append({'variable': key, 'type': type, 'name': name})
#
#   return output


def parse(text, parameters):

  # parse JSON into dictionary
  text_dictionary = yaml.safe_load(text)

  # save the data in the parameters to be used by the GUI
  parameters['Inputs']['FaultHandler']['data'] = text_dictionary

  # print
  if parameters['Inputs']['FaultHandler']['showYAML']:
    Utilities.printParameters(text_dictionary, parameters)

  try:
    # open template file
    with open(os.path.dirname(os.path.realpath(__file__)) + '/Support/fault_handler.rol.template', 'r') as file:
      template = Template(file.read())

    # render the template with the data
    rol_code = template.render(text=text_dictionary)

    # print
    if parameters['Inputs']['FaultHandler']['showRol']:
      Utilities.printSource(rol_code, 'coffeescript', parameters)

    # parse generated rol code
    code, parameters = RoL.parse('block(' + rol_code + ')', parameters)
  except Exception as e:
    print e

  if parameters['Inputs']['FaultHandler']['showXML']:
    Utilities.printCode(code, parameters)


  # code = etree.fromstring('<hello></hello>')

  # # convert into more descriptive dictionary
  # discriptive_dictionary = convertParameters(text_dictionary)

  # if parameters['Inputs']['FaultHandler']['showYAML']:
  #   Utilities.printParameters(discriptive_dictionary, parameters)


  # code = etree.fromstring(DictionaryToXML.dicttoxml(text_dictionary, namespace='fth'))
  #
  # if parameters['Inputs']['FaultHandler']['showXML']:
  #   Utilities.printCode(code, parameters)


  # # extract code
  # discriptive_dictionary['nodes_xml'] = DictionaryToXML.dicttoxml(text_dictionary['faults'], namespace='fh')
  #
  # if parameters['Inputs']['FaultHandler']['showXML']:
  #   Utilities.printCode(etree.fromstring(discriptive_dictionary['nodes_xml']), parameters)
  #
  # # open template file
  # with open(Utilities.myPluginPath(parameters) + '/Support/fault_handler.rol.template', 'r') as file:
  #   template = Template(file.read())
  #
  # # render the template with the data
  # rol_code = template.render(**discriptive_dictionary)
  #
  # # print intermediate rol code is requested
  # if parameters['Inputs']['FaultHandler']['showRol']:
  #   Utilities.printSource(rol_code, 'coffeescript', parameters)
  #
  #
  # # parse generated rol code
  # code, parameters = RoL.parse(rol_code, parameters)
  #
  # # add fault detection gui to the outputs
  # outputs = Utilities.ensureList(parameters['globals']['output'])
  # outputs.append('FaultHandler')
  # parameters['globals']['output'] = outputs

  return code, parameters
