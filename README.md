# CLIMR Translation 

This repository contains scripts for the CLIMR translation workflow.

## Workflow overview

* Export survey from Qualtrics as a .qsf
* Generate excel translation template
* Translate
* Validate translation
* Generate new .qsf file(s)
* Create lab-specific .qsf file(s)

## Installation
The scripts requires python 3.8 > and pip for installing requirements.

Run:
<pre>pip install -r requirements.txt</pre>

## Generate excel translation template
Use *generate_translation_template.py* for generating an Excel template

**Arguments:**
* -q *Path to .qsf file* 
* -o *Path to output Excel file*
* -s *Strips all html from question texts (optional)*

<pre>
python generate_translation_template.py -q ./path/to/survey.qsf -o ./path/to/template.xlsx
</pre>

## Generate new .qsf file(s)

Use *generate_qsf_translation_all_studies.py* for generating a new translated .qsf that will be used as master for a specific language

The script uses a settings file in json format for batch-processing 

Example settings.json:
<pre>
{
  "1": {
    "name": "temporal",
    "path": "qsf/climr_temporal_en_template.qsf",
    "data": {
      "em": {}
    }
  },
  "2": {
    "name": "spatial",
    "path": "qsf/climr_spatial_en_template.qsf",
    "data": {
      "em": {}
    }
  },
  "3": {
    "name": "social",
    "exclude": ["QID90", "QID91", "QID92", "QID94","QID95"],
    "path": "qsf/climr_social_en_template.qsf",
    "data": {
      "em": {}
    }
  },
  "4": {
    "name": "likelihood",
    "path": "qsf/climr_likelihood_en_template.qsf",
    "data": {
      "em": {}
    }
  }
}
</pre>

**Arguments:**
* -x *Path to input translation Excel file*
* -s *Path to settings.json*
* -l *Survey target language code. e.g. SV, EN"*

<pre>
python generate_qsf_translation_all_studies.py -x path/to/translated.xlsx -s path/to/settings.json -l SV
</pre>

## Create lab-specific .qsf file(s)

Use *get_lab_specific_data.py* for updating the .qsf files generated in the previous step. 
The script fetches the lab specific data through Baserow's API. The api-call the scripts executes needs to be 
authenticated so an api token needs to be generated in Baserow and added to the script. Refer to 
[Baserows Documentation](https://baserow.io/user-docs/personal-api-tokens) for how to generate personal API-Tokens. 

**Arguments:**
* -i *Path to input directory containing .qsf files*
* -l *Lab ID*


<pre>python get_lab_specific_data.py -i path/to/directory -l SE_01  </pre>
