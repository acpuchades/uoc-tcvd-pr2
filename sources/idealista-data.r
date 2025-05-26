library(missRanger)
library(stopwords)
library(tidytext)
library(tidyverse)

datos <- read_csv("data/idealista-sale-properties-spain.csv")

normalize_address <- function(x) {
  x |>
    str_to_upper() |>
    stringi::stri_trans_general("Latin-ASCII") |>
    str_replace_all("C/", "CALLE ") |>
    str_replace_all("CARRER", "CALLE ") |>
    str_replace_all("AV/", "AVENIDA ") |>
    str_replace_all("AV.", "AVENIDA ") |>
    str_replace_all("AVINGUDA", "AVENIDA ") |>
    str_replace_all("\\s+", " ") |>
    str_replace_all(",+", ",") |>
    str_trim()
}

extract_calle <- function(x) {
  norm_address <- normalize_address(x)
  norm_address |>
    str_extract("^([^,0-9]+)") |>
    str_replace("S/N", "") |>
    str_trim()
}

extract_provincia <- function(x) {
  address_parts <- normalize_address(x) |> str_split(",")
  map_chr(address_parts, function(parts) {
    if (length(parts) >= 2) {
      str_trim(parts[length(parts)])
    } else {
      NA_character_
    }
  })
}

extract_ciudad <- function(x) {
  address_parts <- normalize_address(x) |> str_split(",")
  map_chr(address_parts, function(parts) {
    if (length(parts) >= 3) {
      str_trim(parts[length(parts) - 1])
    } else {
      NA_character_
    }
  })
}

extract_distrito <- function(x) {
  norm_address <- normalize_address(x)
  address_parts <- str_split(norm_address, ",")
  map_chr(seq_along(norm_address), function(i) {
    addr <- norm_address[i]
    parts <- address_parts[[i]]
    if (str_detect(addr, "DISTRITO")) {
      str_extract(addr, "DISTRITO [^,]+")
    } else if (length(parts) >= 4) {
      str_trim(parts[length(parts) - 2])
    } else {
      NA_character_
    }
  })
}

extract_barrio <- function(x) {
  norm_address <- normalize_address(x)
  address_parts <- str_split(norm_address, ",")
  map_chr(seq_along(norm_address), function(i) {
    addr <- norm_address[i]
    parts <- address_parts[[i]]
    if (str_detect(addr, "BARRIO")) {
      str_extract(addr, "BARRIO [^,]+")
    } else if (length(parts) >= 5) {
      str_trim(parts[length(parts) - 3])
    } else {
      NA_character_
    }
  })
}

datos_ext <- datos |>
	mutate(
		calle = extract_calle(address),
		barrio = extract_barrio(address),
		distrito = extract_distrito(address),
		ciudad = extract_ciudad(address),
		provincia = extract_provincia(address),
		superficie = features |>
		    str_to_lower() |>
		    str_extract("([0-9]+) m²", group=1),
		habitaciones = features |>
		    str_to_lower() |>
		    str_extract("([0-9]+) hab.", group=1),
		piso = case_when(
		    features |> str_to_lower() |> str_detect("bajo") ~ "B",
		    features |> str_to_lower() |> str_detect("entreplanta") ~ "E",
		    TRUE ~ features |> str_to_lower() |> str_extract("planta ([0-9]+)[ºª]", group=1),
		),
		ascensor = features |>
		    str_to_lower() |>
		    str_extract("(con|sin) ascensor", group=1) |>
		    case_match("con" ~ TRUE, "sin" ~ FALSE, .default=FALSE),
		exterior = features |>
		    str_to_lower() |>
		    str_extract("(exterior|interior)", group=1) |>
		    case_match("exterior" ~ TRUE, "interior" ~ FALSE, .default=FALSE),
		terraza = description |> str_detect(regex("terraza", ignore_case=TRUE)),
		garaje = features |> str_to_lower() |> str_detect("garaje"),
	)

datos_conv <- datos_ext |>
	mutate(
	    property_id = as.character(property_id),
	    price = price |> str_remove("\\.") |> as.numeric(),
	    price_m2 = price_m2 |> str_remove("\\.") |> str_remove(" €/m²") |> as.numeric(),
	    across(c(habitaciones, superficie), as.numeric),
	    across(c(calle, barrio, distrito, ciudad, provincia, piso),
	            ~ .x |> str_to_upper() |> as.factor()),
	    across(c(ascensor, exterior, garaje, terraza), ~if_else(.x, "S", "N") |> factor(levels = c("N", "S"))),
		across(starts_with("energy_"), ~ na_if(.x, 9999)),
		across(c(price, price_m2, superficie), ~ na_if(.x, 0)),
)

datos_imp <- missRanger(
  datos_conv, data_only = TRUE,
  formula = superficie + energy_consumption + energy_emissions +
            piso + ascensor + garaje + exterior + habitaciones +
            calle + barrio + distrito + ciudad + provincia + terraza ~
    . - title - description - features - property_id - property_url
      - address - agent_ref - last_updated - scraped_date,
  num.trees = 50, max.depth = 5, pmm.k = 5, seed = 123,
)

dir.create("output", showWarnings=FALSE)
write_csv(datos_imp, "output/idealista-sale-properties-spain_processed.csv")
