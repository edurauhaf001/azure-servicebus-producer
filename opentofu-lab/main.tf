terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>4.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

resource "azurerm_servicebus_namespace" "sb" {
  name                = "sb-2510876014-tofu"
  location            = var.location
  resource_group_name = var.resource_group

  sku = "Standard"
}

resource "azurerm_servicebus_topic" "orders" {
  name         = "orders"
  namespace_id = azurerm_servicebus_namespace.sb.id
}

resource "azurerm_servicebus_subscription" "everything" {
  name               = "everything"
  topic_id           = azurerm_servicebus_topic.orders.id
  max_delivery_count = 10
}

resource "azurerm_servicebus_subscription" "error" {
  name               = "error"
  topic_id           = azurerm_servicebus_topic.orders.id
  max_delivery_count = 10
}

resource "azurerm_servicebus_subscription_rule" "error_filter" {
  name            = "error-filter"
  subscription_id = azurerm_servicebus_subscription.error.id

  filter_type = "SqlFilter"
  sql_filter  = "severity = 'error'"
}