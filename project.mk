#Project specific values
YAML_DIRECTORY?=deploy
SELECTOR_SYNC_SET_TEMPLATE_DIR?=scripts/templates/
GIT_ROOT?=$(shell git rev-parse --show-toplevel 2>&1)

# WARNING: REPO_NAME will default to the current directory if there are no remotes
REPO_NAME=managed-cluster-config

#Script variables
GEN_TEMPLATE?=scripts/generate_template.py -t ${SELECTOR_SYNC_SET_TEMPLATE_DIR} -y ${YAML_DIRECTORY} -d ${GIT_ROOT}/hack/ -r ${REPO_NAME}
GEN_HCP_POLICY?=scripts/generate-hcp-policy.sh
GEN_HCP_POLICY_CONFIG?=scripts/generate-policy-config-hcp.py
GEN_HOSTED_POLICY_CONFIG_SP?=scripts/generate-subjectpermissions-policy-config.py
GEN_HOSTED_POLICY?=scripts/generate-hostedcluster-policy.sh
GEN_HOSTED_POLICY_CONFIG?=scripts/generate-policy-config-hostedcluster.py
