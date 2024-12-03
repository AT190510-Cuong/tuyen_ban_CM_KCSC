require("dotenv").config();

const Config = {
    JWT_SECRET: process.env.JWT_SECRET || "cryptocatisthebest!",
    JWT_ALGORITHM: "RS256",
    DATABASE_URL: `postgresql://${process.env.POSTGRES_USER}:${process.env.POSTGRES_PASSWORD}@${process.env.POSTGRES_HOST}/${process.env.POSTGRES_DB}`,
};

module.exports = Config;
