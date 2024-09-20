
CREATE DATABASE keywords_subscription;

CREATE TABLE keyword (
    keyword_id BIGINT AUTO_INCREMENT,
    keyword_name VARCHAR(255),
    PRIMARY KEY (keyword_id)
);

ALTER TABLE keyword ADD UNIQUE (keyword_name);

CREATE TABLE keyword_search_volume (
    keyword_id BIGINT,
    created_datetime DATETIME,
    search_volume BIGINT,
    PRIMARY KEY (keyword_id, created_datetime),
    FOREIGN KEY (keyword_id) REFERENCES keyword(keyword_id)
);

CREATE TABLE user_subscription (
    user_id BIGINT,
    keyword_id BIGINT,
    timing VARCHAR(45),
    subscription_start DATETIME,
    subscription_end DATETIME,
    PRIMARY KEY (user_id, keyword_id),
    FOREIGN KEY (keyword_id) REFERENCES keyword(keyword_id)
);

